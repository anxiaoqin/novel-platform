#!/usr/bin/env python3
"""
清理《异界归来：核弹砸脸》全书正文中的异常标记（第六轮）
处理遗漏的大纲列表内容
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
    i = 0
    
    while i < len(lines):
        line = lines[i]
        stripped = line.strip()
        
        # 检查是否是"锚点事件"或"章节禁区"章节的列表内容
        # 这些内容前两行是大纲标记，后面的1. 2. 3. 4.列表需要删除
        if '锚点事件' in stripped or '章节禁区' in stripped:
            # 跳过后续的列表内容（1. 2. 3. 4. 开头的内容）
            j = i + 1
            while j < len(lines):
                next_stripped = lines[j].strip()
                # 继续检查后续行是否是列表格式
                if re.match(r'^\d+\.', next_stripped):
                    deleted_count += 1
                    j += 1
                elif next_stripped == '':
                    # 空行也跳过
                    j += 1
                else:
                    break
            i = j
            continue
        
        new_lines.append(line)
        i += 1
    
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
    modified_files = []
    
    print("=" * 70)
    print("开始清理第六轮 - 列表内容清理")
    print("=" * 70)
    
    for volume_dir in volumes:
        volume_name = volume_dir.name
        
        txt_files = sorted([f for f in volume_dir.glob("*.txt")])
        
        for txt_file in txt_files:
            d = process_file(txt_file)
            total_deleted += d
            if d > 0:
                modified_files.append((volume_name, txt_file.name, d))
    
    print(f"\n第六轮清理完成！")
    print(f"  - 删除 {total_deleted} 处列表内容")
    
    if modified_files:
        print("\n修改的文件：")
        for vol, fname, count in modified_files:
            print(f"  [{vol}] {fname}: 删除{count}行")
    
    print("=" * 70)

if __name__ == "__main__":
    main()
