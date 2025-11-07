# Cache 文件目录结构说明

## 目录组织

```
SearchPaperByEmbedding/
├── cache/                           # Cache 文件目录
│   ├── cache_*.npy                 # Embedding cache 文件
│   ├── merged_papers_*.json        # 合并的论文数据文件
│   └── temp_merged.json           # 临时合并文件
├── demo.py                         # 主程序入口
├── search.py                       # 搜索功能模块
└── ...
```

## 文件命名规则

### Embedding Cache 文件
- 格式: `cache_{papers_file_base}_{hash}_{model_type}.npy`
- 例如: `cache_merged_papers_1762478450_924370ce_api.npy`
- `{papers_file_base}`: 原始论文文件的基础名称
- `{hash}`: 基于论文文件路径生成的MD5哈希值（前8位）
- `{model_type}`: 模型类型 (`api`, `openai`, 或本地模型)

### 合并论文文件
- 格式: `merged_papers_{timestamp}.json`
- 例如: `merged_papers_1762478450.json`
- `{timestamp}`: 创建时的时间戳

## 路径处理

### 自动创建Cache目录
- 程序会自动创建 `cache/` 目录
- 如果目录不存在，会自动创建

### Cache文件路径
- 所有cache文件都保存在 `cache/` 目录中
- 不再散落在项目根目录

### 兼容性
- 支持相对路径和绝对路径
- 自动处理路径分隔符（Windows/Linux兼容）

## 使用说明

1. **创建新的数据集**: 运行 `python demo.py` 选择论文文件，合并后的数据会保存到 `cache/merged_papers_{timestamp}.json`

2. **自动加载Cache**: 程序会自动检查是否存在对应的embedding cache文件，如果存在则直接加载

3. **手动清理**: 可以删除 `cache/` 目录下的文件来重新计算embeddings

4. **备份重要数据**: 建议定期备份 `cache/` 目录下的重要文件

## 注意事项

- Cache文件可能较大（几MB到几百MB），确保有足够的磁盘空间
- 修改论文文件后，需要重新计算embeddings（旧cache会自动失效）
- Cache文件是平台相关的，不同操作系统之间可能不兼容