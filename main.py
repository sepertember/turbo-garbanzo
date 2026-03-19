"""
文件元数据备份工具 - 程序入口

该程序扫描指定的输入目录，递归获取所有文件，计算每个文件的SHA-256哈希值，
并记录元数据（路径、大小、修改时间）。然后根据backup_rules.json规则文件
决定哪些文件需要备份到输出目录，最后生成一份包含所有处理文件信息的JSON报告。
"""
import os
import sys

# 确保可以导入本地模块
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from config.settings import INPUT_DIR, OUTPUT_DIR
from utils.file_utils import validate_input_directory, ensure_directory_exists
from core.scanner import scan_directory, get_absolute_path
from core.hasher import calculate_sha256
from core.backup import load_backup_rules, backup_files
from core.reporter import create_report_data, generate_report


def main():
    """
    主函数：协调各模块完成备份任务
    """
    print("=" * 60)
    print("文件元数据备份工具")
    print("=" * 60)
    
    # 1. 验证输入目录
    print(f"\n[1/5] 验证输入目录: {INPUT_DIR}")
    validate_input_directory(INPUT_DIR)
    print("  ✓ 输入目录验证通过")
    
    # 2. 确保输出目录存在
    print(f"\n[2/5] 确保输出目录存在: {OUTPUT_DIR}")
    ensure_directory_exists(OUTPUT_DIR)
    print("  ✓ 输出目录准备就绪")
    
    # 3. 扫描输入目录
    print(f"\n[3/5] 扫描输入目录...")
    file_list = scan_directory(INPUT_DIR)
    print(f"  ✓ 发现 {len(file_list)} 个文件")
    
    if not file_list:
        print("\n  警告: 输入目录为空，没有文件需要处理")
        return
    
    # 4. 加载备份规则
    print(f"\n[4/5] 加载备份规则...")
    rules = load_backup_rules()
    print(f"  ✓ 加载了 {len(rules)} 条备份规则")
    
    # 5. 计算哈希值并执行备份
    print(f"\n[5/5] 处理文件（计算哈希值并备份）...")
    file_hashes = {}
    backed_up_files = []
    
    for i, relative_path in enumerate(file_list, 1):
        abs_path = get_absolute_path(relative_path, INPUT_DIR)
        
        # 计算哈希值
        file_hash = calculate_sha256(abs_path)
        if file_hash:
            file_hashes[relative_path] = file_hash
        
        # 显示进度
        if i % 10 == 0 or i == len(file_list):
            print(f"  进度: {i}/{len(file_list)} 文件已处理")
    
    # 执行备份
    backed_up_files = backup_files(file_list, rules, INPUT_DIR, OUTPUT_DIR)
    print(f"  ✓ 已备份 {len(backed_up_files)} 个文件")
    
    # 6. 生成报告
    print(f"\n[6/6] 生成报告...")
    report_data = create_report_data(
        file_list,
        file_hashes,
        backed_up_files,
        INPUT_DIR,
    )
    
    success = generate_report(report_data)
    if success:
        print(f"  ✓ 报告已生成: {os.path.join(OUTPUT_DIR, 'backup_report.json')}")
    else:
        print(f"  ✗ 报告生成失败")
    
    # 7. 打印摘要
    print("\n" + "=" * 60)
    print("处理摘要")
    print("=" * 60)
    print(f"总文件数:     {len(file_list)}")
    print(f"成功计算哈希: {len(file_hashes)}")
    print(f"已备份文件:   {len(backed_up_files)}")
    print(f"跳过备份:     {len(file_list) - len(backed_up_files)}")
    print("=" * 60)
    print("备份任务完成！")
    print("=" * 60)


if __name__ == "__main__":
    main()
