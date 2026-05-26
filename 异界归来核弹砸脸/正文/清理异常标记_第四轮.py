#!/usr/bin/env python3
"""
清理《异界归来：核弹砸脸》全书正文中的异常标记（第四轮）
处理遗漏的大纲格式：
- - **时间**：xxx 等元信息行
- **目标**：xxx 等目标/冲突/解决格式
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
    modified_count = 0
    new_lines = []
    
    for line in lines:
        original_line = line
        stripped = line.strip()
        
        # 1. - **时间**：xxx 等元信息行 - 删除
        if re.match(r'^- \*\*[^*]+\*\*[:：]', stripped):
            deleted_count += 1
            continue
        
        # 2. **目标**：xxx 等独立行 - 删除
        if re.match(r'^\*\*[^*]+\*\*[:：]', stripped):
            deleted_count += 1
            continue
        
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
    
    return deleted_count, modified_count

def main():
    """主函数"""
    volumes = sorted([d for d in PROJECT_ROOT.iterdir() if d.is_dir()], 
                    key=lambda x: x.name)
    
    total_deleted = 0
    total_modified = 0
    
    print("=" * 70)
    print("开始清理第四轮 - 大纲格式清理")
    print("=" * 70)
    
    for volume_dir in volumes:
        volume_name = volume_dir.name
        
        txt_files = sorted([f for f in volume_dir.glob("*.txt")])
        
        for txt_file in txt_files:
            d, m = process_file(txt_file)
            total_deleted += d
            total_modified += m
    
    print(f"\n第四轮清理完成！")
    print(f"  - 删除 {total_deleted} 处大纲格式")
    print(f"  - 修改 {total_modified} 处")
    print("=" * 70)

if __name__ == "__main__":
    main()
