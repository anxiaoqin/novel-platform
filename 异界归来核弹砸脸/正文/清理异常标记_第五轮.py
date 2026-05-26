#!/usr/bin/env python3
"""
清理《异界归来：核弹砸脸》全书正文中的异常标记（第五轮）
处理遗漏的格式：
- **** 分隔符
- **锚点事件** 等大纲格式
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
        
        # 1. **** 分隔符 - 删除
        if stripped == '****':
            deleted_count += 1
            continue
        
        # 2. **锚点事件** 等大纲格式 - 删除
        if re.match(r'^\*\*锚点事件\*\*', stripped):
            deleted_count += 1
            continue
        
        if re.match(r'^\*\*章节禁区\*\*', stripped):
            deleted_count += 1
            continue
        
        # 3. 章节完结标记 **（第X章 xxx 完）** -> 改为正常格式
        match = re.match(r'^\*\*\（(.+?)完\）\*\*$', stripped)
        if match:
            inner = match.group(1)
            new_line = f"（{inner}完）\n"
            modified_count += 1
            new_lines.append(new_line)
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
    modified_files = []
    
    print("=" * 70)
    print("开始清理第五轮 - 最终清理")
    print("=" * 70)
    
    for volume_dir in volumes:
        volume_name = volume_dir.name
        
        txt_files = sorted([f for f in volume_dir.glob("*.txt")])
        
        for txt_file in txt_files:
            d, m = process_file(txt_file)
            total_deleted += d
            total_modified += m
            if m > 0:
                modified_files.append((volume_name, txt_file.name))
    
    print(f"\n第五轮清理完成！")
    print(f"  - 删除 {total_deleted} 处格式")
    print(f"  - 修改 {total_modified} 处章节完结标记")
    
    if modified_files:
        print("\n修改的章节完结标记：")
        for vol, fname in modified_files:
            print(f"  [{vol}] {fname}")
    
    print("=" * 70)

if __name__ == "__main__":
    main()
