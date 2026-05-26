#!/usr/bin/env python3
"""
清理《异界归来：核弹砸脸》全书正文中的异常标记（第三轮）
处理遗漏的标题：
- ### 夜最深时 等小标题
- ### 附加场景：xxx 等附加场景标题
- ## 第412章 xxx 等错误格式的章节标题
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
        
        # 1. ### 夜最深时 / ### 意志之墙 等小标题 - 删除
        if re.match(r'^### +[^\s]+', stripped):
            deleted_count += 1
            continue
        
        # 2. ### 附加场景：xxx - 删除
        if re.match(r'^### +附加场景[：:：]', stripped):
            deleted_count += 1
            continue
        
        # 3. ## 第X章 xxx 等错误格式的章节标题 - 去掉## 
        if re.match(r'^## +第[一二三四五六七八九十百\d]+章', stripped):
            new_line = re.sub(r'^## +', '', stripped)
            modified_count += 1
            new_lines.append(new_line + '\n')
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
    print("开始清理第三轮 - 最终补充")
    print("=" * 70)
    
    modified_files = []
    
    for volume_dir in volumes:
        volume_name = volume_dir.name
        
        txt_files = sorted([f for f in volume_dir.glob("*.txt")])
        
        for txt_file in txt_files:
            d, m = process_file(txt_file)
            total_deleted += d
            total_modified += m
            if m > 0:
                modified_files.append((volume_name, txt_file.name))
    
    print(f"\n第三轮清理完成！")
    print(f"  - 删除 {total_deleted} 处标题")
    print(f"  - 修改 {total_modified} 处章节标题格式")
    
    if modified_files:
        print("\n修改的章节标题格式：")
        for vol, fname in modified_files:
            print(f"  [{vol}] {fname}")
    
    print("=" * 70)

if __name__ == "__main__":
    main()
