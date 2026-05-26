#!/usr/bin/env python3
"""
清理《异界归来：核弹砸脸》全书正文中的异常标记（第七轮）
处理遗漏的大纲列表内容：章节开头的数字列表（锚点事件/章节禁区内容）
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
        
        # 检查是否是章节开头的大纲列表内容
        # 模式：章节标题后的连续数字列表（1. 2. 3. 4.）
        # 只处理章节开头附近（前30行内）的情况
        if i < 30:
            # 检查是否是数字列表项
            if re.match(r'^\d+\.', stripped):
                # 这可能是大纲列表，验证上下文
                # 向上查找是否有类似"锚点事件"或"章节禁区"的标记（已被删除）
                is_outline_list = False
                
                # 检查后续是否有连续的列表项
                j = i
                list_items = []
                while j < len(lines) and j < i + 10:
                    next_stripped = lines[j].strip()
                    if re.match(r'^\d+\.', next_stripped):
                        list_items.append(j)
                        j += 1
                    elif next_stripped == '':
                        # 空行可能是分隔
                        j += 1
                    else:
                        break
                
                # 如果有4个或更多连续的列表项，认为是大纲内容
                if len(list_items) >= 4:
                    # 这是大纲列表，删除这些行
                    for idx in list_items:
                        deleted_count += 1
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
    print("开始清理第七轮 - 大纲列表内容清理")
    print("=" * 70)
    
    for volume_dir in volumes:
        volume_name = volume_dir.name
        
        txt_files = sorted([f for f in volume_dir.glob("*.txt")])
        
        for txt_file in txt_files:
            d = process_file(txt_file)
            total_deleted += d
            if d > 0:
                modified_files.append((volume_name, txt_file.name, d))
    
    print(f"\n第七轮清理完成！")
    print(f"  - 删除 {total_deleted} 处大纲列表内容")
    
    if modified_files:
        print("\n修改的文件：")
        for vol, fname, count in modified_files:
            print(f"  [{vol}] {fname}: 删除{count}行")
    
    print("=" * 70)

if __name__ == "__main__":
    main()
