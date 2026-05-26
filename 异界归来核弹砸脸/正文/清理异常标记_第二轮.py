#!/usr/bin/env python3
"""
清理《异界归来：核弹砸脸》全书正文中的异常标记（第二轮）
补充处理遗漏的标题类型：
- ## 一 / ## 三 等单独数字标题
- ## 场景一：xxx / ## 场景二：xxx 等场景标题
- ## 第一段 / ## 第二段 等段落标题
"""

import re
from pathlib import Path

# 项目根目录
PROJECT_ROOT = Path("小说创作/异界归来核弹砸脸/正文/")

def process_file(filepath):
    """处理单个文件"""
    with open(filepath, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    deleted_count = 0
    new_lines = []
    
    for line in lines:
        original_line = line
        stripped = line.strip()
        
        # 需要删除的标题类型
        delete_patterns = [
            # ## 单独数字（一、二、三...）
            r'^## +[一二三四五六七八九十百]+$',
            # ## 场景X：xxx
            r'^## +场景[一二三四五六七八九十零\d]+[：:：]',
            # ## 第X段
            r'^## +第[一二三四五六七八九十百\d]+段$',
            # ## 第X节：xxx
            r'^## +第[一二三四五六七八九十百\d]+节[：:：]',
        ]
        
        should_delete = False
        for pattern in delete_patterns:
            if re.match(pattern, stripped):
                should_delete = True
                deleted_count += 1
                break
        
        if not should_delete:
            new_lines.append(line)
    
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
    
    return deleted_count

def main():
    """主函数"""
    volumes = sorted([d for d in PROJECT_ROOT.iterdir() if d.is_dir()], 
                    key=lambda x: x.name)
    
    total_deleted = 0
    
    print("=" * 70)
    print("开始清理第二轮 - 遗漏的Markdown标题")
    print("=" * 70)
    
    for volume_dir in volumes:
        volume_name = volume_dir.name
        volume_deleted = 0
        
        txt_files = sorted([f for f in volume_dir.glob("*.txt")])
        
        for txt_file in txt_files:
            count = process_file(txt_file)
            volume_deleted += count
            total_deleted += count
    
    print(f"\n第二轮清理完成！共删除 {total_deleted} 处遗漏的标题")
    print("=" * 70)

if __name__ == "__main__":
    main()
