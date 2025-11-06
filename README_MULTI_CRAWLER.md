# Multi-Conference Paper Crawler

一个支持多个主流CCF-A会议的论文爬虫，能够按decision类型分类爬取论文。

## 功能特性

- ✅ **多会议支持**: NeurIPS, ICML, ICLR等主流CCF-A会议
- ✅ **多年份支持**: 支持2023-2025年等多个年份
- ✅ **交互式选择**: 启动后可选择会议和年份
- ✅ **智能分类**: 自动按论文类型（oral、spotlight、poster）分类
- ✅ **高效爬取**: 直接按decision类型分别爬取，避免下载不必要的数据
- ✅ **完整数据**: 包含标题、作者、摘要、关键词等完整信息

## 支持的会议

| 会议 | 年份范围 | 决策类型 | API状态 |
|------|----------|----------|---------|
| NeurIPS | 任意年份 (2000-2030) | oral, spotlight, poster | ✅ 完全支持 |
| ICML | 任意年份 (2000-2030) | 通用分类 | ✅ 支持 |
| ICLR | 任意年份 (2000-2030) | 通用分类 | ✅ 支持 |

**注意**: 年份不再受限制，可以自由输入任何合理的年份。

## 使用方法

### 方法1: 交互式运行

```bash
python multi_conference_crawler.py
```

运行后会提示选择：
1. 会议名称 (NeurIPS, ICML, ICLR)
2. 年份 (自由输入，如 2025, 2024, 2023, 2022 等)
3. 输出目录

**年份输入示例**:
- 2025 (最新)
- 2024 (最近)
- 2023 (往年)
- 2022 (更早年份)
- 任何2000-2030之间的年份

### 方法2: 编程方式使用

```python
from multi_conference_crawler import MultiConferenceCrawler

# 创建爬虫实例
crawler = MultiConferenceCrawler()

# 爬取任意年份的论文
papers_by_decision, all_papers = crawler.crawl_conference_by_decision(
    conference="NeurIPS",
    year=2024,  # 可以是任何年份：2025, 2024, 2023, 2022, etc.
    output_dir="my_papers"
)

# 更多示例：
# crawler.crawl_conference_by_decision("NeurIPS", 2025, "papers2025")
# crawler.crawl_conference_by_decision("ICML", 2024, "icml_papers")
# crawler.crawl_conference_by_decision("ICLR", 2023, "iclr_2023")

print(f"总共爬取 {len(all_papers)} 篇论文")
for decision, papers in papers_by_decision.items():
    print(f"{decision}: {len(papers)} 篇")
```

### 方法3: 演示脚本

```bash
# 快速演示（NeurIPS 2024）
python demo_multi_crawler.py
# 选择选项 1

# 批量演示（所有会议）
python demo_multi_crawler.py
# 选择选项 2
```

## 输出文件结构

爬取完成后，会在指定目录下创建如下结构：

```
output_dir/
├── neurips_2024/
│   ├── neurips_2024_oral.json      # 口头报告论文
│   ├── neurips_2024_spotlight.json # 聚光灯报告论文
│   ├── neurips_2024_poster.json    # 海报展示论文
│   └── neurips_2024_all.json       # 所有论文
├── icml_2024/
│   ├── icml_2024_accepted.json      # 接收论文
│   └── icml_2024_all.json          # 所有论文
└── ...
```

## 数据格式

每篇论文包含以下字段：

```json
{
  "id": "论文ID",
  "number": "论文编号",
  "title": "论文标题",
  "authors": ["作者1", "作者2", ...],
  "abstract": "论文摘要",
  "keywords": ["关键词1", "关键词2", ...],
  "primary_area": "主要研究领域",
  "venue": "会议名称+类型",
  "decision": "决策类型",
  "forum_url": "论文链接"
}
```

## API频率限制

OpenReview API有频率限制，爬虫已内置：
- 请求间隔：1秒
- 错误重试机制
- 分批处理

如遇到429错误，请等待一段时间后重试。

## 扩展支持其他会议

要添加新会议支持，修改 `ConferenceConfig.CONFERENCES` 配置：

```python
CONFERENCES = {
    "新会议名": {
        "name": "会议全名",
        "years": [2025, 2024],
        "venue_pattern": "会议域名/{year}/Conference",
        "decision_patterns": {
            "oral": "会议 {year} oral",
            "spotlight": "会议 {year} spotlight",
            "poster": "会议 {year} poster"
        }
    }
}
```

## 注意事项

1. **网络连接**: 需要稳定的网络连接访问OpenReview API
2. **存储空间**: 大型会议可能产生数GB的数据
3. **运行时间**: 完整爬取可能需要数小时
4. **API限制**: 遵守OpenReview API的使用条款和频率限制

## 故障排除

### 常见问题

1. **429 Too Many Requests**
   - 等待几分钟后重试
   - 减少并发请求数量

2. **Connection Timeout**
   - 检查网络连接
   - 增加超时时间设置

3. **No papers found**
   - 确认会议和年份组合存在
   - 检查API端点是否正确

### 联系支持

如遇到问题，请检查：
1. 网络连接状态
2. API端点是否可访问
3. 输出目录权限
4. 存储空间是否充足

## 许可证

本项目遵循开源许可证，请遵守相关使用条款。