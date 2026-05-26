#!/usr/bin/env python3
"""
清理《异界归来：核弹砸脸》全书正文中的异常标记
"""

import os
import re
from pathlib import Path

# 项目根目录
PROJECT_ROOT = Path("小说创作/异界归来核弹砸脸/正文/")

# 统计变量
stats = {}

def is_chapter_title(line):
    """判断是否是章节标题行（需要保留）"""
    line = line.strip()
    # 匹配 "第X章" 或 "第X章：xxx" 或 "第X章 xxx"
    if re.match(r'^第[一二三四五六七八九十百千万\d]+章[：:\s]', line):
        return True
    return False

def is_outline_bracket(line):
    """判断【】标记是否是大纲/结构标记（必须删除整行）"""
    line = line.strip()
    
    # 排除行内包含【】的情况（如 "三、穿越者的身份——【数据删除】"）
    if '——【' in line and line.count('【') == 1 and line.count('】') == 1:
        # 检查【】是否在行内而非独立成行
        if not (line.startswith('【') and line.endswith('】')):
            return False
    
    # 检查是否是独立的大纲标记行
    outline_patterns = [
        r'^【开篇交代】$',
        r'^【场景[〇零一二三四五六七八九十百\d]+[：:].*】$',
        r'^【章节收束】$',
        r'^【段[〇零一二三四五六七八九十百\d]+[：:].*】$',
        r'^## 【小说正文】$',
        r'^## 【章节卫星定位】$',
    ]
    
    for pattern in outline_patterns:
        if re.match(pattern, line):
            return True
    
    # 检查是否是大纲标记（不以对话/台词形式出现）
    # 大纲标记通常在行首且单独成行
    if line.startswith('【') and line.endswith('】'):
        inner = line[1:-1]
        # 大纲标记特征：不包含感叹号开头、不包含问号开头的情绪词
        # 常见大纲词：开篇、场景、章节、段
        outline_keywords = ['开篇', '场景', '章节', '段', '锚点', '情节', '新增', '收束']
        for kw in outline_keywords:
            if kw in inner:
                return True
    
    return False

def process_file(filepath):
    """处理单个文件"""
    with open(filepath, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    original_count = len(lines)
    deleted_lines = []
    modified_lines = []
    
    new_lines = []
    
    for i, line in enumerate(lines):
        original_line = line
        line = line.rstrip('\n\r')
        
        # 1. 检查分隔线 --- (独立的3个或更多短横线行)
        if re.match(r'^-{3,}$', line.strip()):
            deleted_lines.append(('---', i+1, line))
            continue
        
        # 2. 检查 Markdown 标题
        stripped = line.strip()
        
        # 2.1 # 第X章 xxx -> 删除# 前缀，保留章节标题
        if re.match(r'^# +第[一二三四五六七八九十百千万\d]+章', stripped):
            new_title = re.sub(r'^# +', '', stripped)
            modified_lines.append(('# 章节标题', i+1, line, new_title))
            new_lines.append(new_title + '\n')
            continue
        
        # 2.2 ## 尾声 -> 删除## 前缀
        if re.match(r'^## +尾声$', stripped):
            new_line = stripped.replace('## ', '')
            modified_lines.append(('## 尾声', i+1, line, new_line))
            new_lines.append(new_line + '\n')
            continue
        
        # 2.3 ## 第一节：xxx / ## 场景一：xxx 等大纲结构标题 -> 删除整行
        if re.match(r'^#{2,3} +第?[一二三四五六七八九十百\d]+节[：:：]', stripped):
            deleted_lines.append(('##/### 大纲标题', i+1, line))
            continue
        
        # 2.4 ### 开篇交代 / ### 场景一 等大纲标题 -> 删除整行
        if re.match(r'^### +', stripped):
            outline_prefixes = ['开篇', '场景', '情节', '段', '锚点', '收束']
            prefix_found = any(stripped.startswith(f'### {p}') for p in outline_prefixes)
            if prefix_found:
                deleted_lines.append(('### 大纲标题', i+1, line))
                continue
        
        # 2.5 ### 一 / ### 二 等数字分段标题 -> 删除整行
        if re.match(r'^### +[一二三四五六七八九十百\d]+$', stripped):
            deleted_lines.append(('### 数字分段', i+1, line))
            continue
        
        # 2.6 ## 第一节：潜入 等第X节标记 -> 删除整行
        if re.match(r'^第[一二三四五六七八九十百\d]+节[：:：]', stripped):
            deleted_lines.append(('第X节标记', i+1, line))
            continue
        
        # 3. 处理【】标记
        if '【' in line:
            # 检查是否是大纲标记
            if is_outline_bracket(line):
                deleted_lines.append(('【大纲标记】', i+1, line))
                continue
            
            # 检查是否行内混合（【】不是整行）
            # 例如：周明远愣了一下，然后迅速调出那行字：【异常标注：xxx】
            # 或：三、穿越者的身份——【数据删除】。
            line_stripped = line.strip()
            if not (line_stripped.startswith('【') and line_stripped.endswith('】')):
                # 行内包含【】，去掉【】但保留其他内容
                # 查找并替换【】为普通文本
                new_line = line
                # 替换【xxx】为xxx
                new_line = re.sub(r'【([^】]*)】', r'\1', new_line)
                modified_lines.append(('【】行内', i+1, line, new_line.rstrip('\n')))
                new_lines.append(new_line)
                continue
            
            # 独立行，整行都是【xxx】
            new_line = re.sub(r'^(\s*)【([^】]*)】(\s*)$', r'\1\2\3', line)
            if new_line != line:
                modified_lines.append(('【】独立行', i+1, line, new_line.rstrip('\n')))
            new_lines.append(new_line)
            continue
        
        new_lines.append(line + '\n')
    
    # 处理连续空行（3个及以上缩减为2个）
    final_lines = []
    blank_count = 0
    for line in new_lines:
        if line.strip() == '':
            blank_count += 1
            if blank_count <= 2:
                final_lines.append(line)
        else:
            blank_count = 0
            final_lines.append(line)
    
    # 写入文件
    with open(filepath, 'w', encoding='utf-8') as f:
        f.writelines(final_lines)
    
    return {
        'file': filepath.name,
        'deleted': len(deleted_lines),
        'modified': len(modified_lines),
        'deleted_details': deleted_lines,
        'modified_details': modified_lines,
        'original_lines': original_count,
        'final_lines': len(final_lines)
    }

def main():
    """主函数"""
    volumes = sorted([d for d in PROJECT_ROOT.iterdir() if d.is_dir()], 
                    key=lambda x: x.name)
    
    total_deleted = 0
    total_modified = 0
    
    all_deleted_details = []
    all_modified_details = []
    
    print("=" * 70)
    print("开始清理《异界归来：核弹砸脸》全书正文中的异常标记")
    print("=" * 70)
    
    for volume_dir in volumes:
        volume_name = volume_dir.name
        stats[volume_name] = {'deleted': 0, 'modified': 0, 'files': 0}
        
        txt_files = sorted([f for f in volume_dir.glob("*.txt")])
        
        for txt_file in txt_files:
            result = process_file(txt_file)
            stats[volume_name]['deleted'] += result['deleted']
            stats[volume_name]['modified'] += result['modified']
            stats[volume_name]['files'] += 1
            
            total_deleted += result['deleted']
            total_modified += result['modified']
            
            if result['deleted'] > 0:
                all_deleted_details.append((volume_name, result['file'], result['deleted_details']))
            if result['modified'] > 0:
                all_modified_details.append((volume_name, result['file'], result['modified_details']))
    
    # 输出统计结果
    print("\n" + "=" * 70)
    print("清理完成！各卷清理统计：")
    print("=" * 70)
    print(f"{'卷名':<15} {'处理文件':<10} {'删除行':<10} {'修改行':<10}")
    print("-" * 50)
    
    for volume_name, vol_stats in sorted(stats.items()):
        print(f"{volume_name:<15} {vol_stats['files']:<10} {vol_stats['deleted']:<10} {vol_stats['modified']:<10}")
    
    print("-" * 50)
    print(f"{'总计':<15} {sum(v['files'] for v in stats.values()):<10} {total_deleted:<10} {total_modified:<10}")
    print("=" * 70)
    
    # 输出修改详情样本
    if all_modified_details:
        print("\n修改行示例（去掉的【】标记）：")
        print("-" * 50)
        count = 0
        for vol, fname, details in all_modified_details:
            for d in details:
                if count >= 20:
                    break
                if d[0] in ['【】独立行', '【】行内']:
                    print(f"  [{vol}] {fname}: {d[1]} -> {d[3]}")
                    count += 1
            if count >= 20:
                break
    
    if all_deleted_details:
        print("\n删除行类型统计：")
        type_count = {}
        for vol, fname, details in all_deleted_details:
            for d in details:
                t = d[0]
                type_count[t] = type_count.get(t, 0) + 1
        for t, c in sorted(type_count.items(), key=lambda x: -x[1]):
            print(f"  {t}: {c}处")

if __name__ == "__main__":
    main()
