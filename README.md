# turbo-garbanzo
# 批量文件格式转换与元数据提取工具

一个基于 Python 标准库开发的批量文本文件处理工具，支持 TXT ↔ CSV 格式互转，自动提取文件元数据并生成处理报告。

## 功能特性

- ✅ **格式转换**: 支持 `.txt` 和 `.csv` 文件相互转换
- ✅ **编码检测**: 自动识别 UTF-8、GBK、GB2312 编码
- ✅ **元数据提取**: 提取创建时间、修改时间、文件大小、编码格式等
- ✅ **容错处理**: 自动跳过空文件或损坏文件并记录原因
- ✅ **报告生成**: 生成 CSV 格式元数据清单和 LOG 格式转换日志

## 目录结构

```
turbo-garbanzo/
├── main.py                  # 程序入口
├── config.py                # 配置信息
├── file_proc_converter.py   # 文件格式转换核心逻辑
├── file_proc_metadata.py    # 元数据提取功能
├── file_proc_encoder.py     # 编码检测与转换
├── logger.py                # 日志记录工具
├── raw_files/               # 输入文件目录（自动创建）
├── converted_files/         # 转换输出目录（自动创建）
└── metadata_reports/        # 元数据和日志目录（自动创建）
```

## 使用方法

### 1. 准备文件
将需要处理的文件放入 `raw_files/` 目录

### 2. 运行程序

**交互式运行**：
```bash
python main.py
```

**命令行直接运行**：
```bash
python main.py TXT2CSV   # TXT 转 CSV
python main.py CSV2TXT   # CSV 转 TXT
```

## 输出说明

### 元数据清单 (`metadata_reports/metadata_list.csv`)
包含以下字段：
- `filename`: 文件名
- `file_path`: 文件路径
- `creation_time`: 创建时间
- `modification_time`: 修改时间
- `file_size_bytes`: 文件大小（字节）
- `encoding`: 编码格式
- `status`: 处理状态
- `reason`: 处理原因/错误信息

### 转换日志 (`metadata_reports/conversion.log`)
每行格式：`时间戳 - 操作类型 - 文件路径 - 结果`

## 技术栈

- **语言**: Python 3.10+
- **依赖**: 仅使用 Python 标准库（无第三方依赖）

## 约束说明

1. **命名规范**: 核心功能文件以 `file_proc_` 为前缀，元数据函数以 `metadata_` 为前缀
2. **目录约束**: 输入输出目录固定，在 `config.py` 中定义为常量
3. **格式要求**: 元数据清单为 CSV 格式，日志为 LOG 格式
