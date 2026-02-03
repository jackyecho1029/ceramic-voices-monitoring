# Ceramic Voices 每日数据搜集监控

## 📊 项目概述

这是一个自动化系统，用于每日搜集 Ceramic Voices 相关的市场数据、竞品信息和行业趋势，并生成分析报告。

## 🚀 功能

- [x] 每日自动数据搜集
- [x] 行业新闻监控
- [x] 趋势分析
- [x] 自动报告生成
- [x] GitHub Actions 集成

## 📁 项目结构

```
ceramic-voices-monitoring/
├── .github/
│   └── workflows/
│       └── daily-report.yml      # GitHub Actions 工作流
├── scrapers/
│   ├── news.py                 # 新闻数据搜集
│   └── trends.py              # 趋势数据搜集
├── analysis/
│   └── daily_analysis.py       # 数据分析脚本
├── reports/
│   ├── generate_report.py       # 报告生成
│   └── output/               # 生成的报告
└── README.md                 # 本文件
```

## 🔄 工作流程

```
每日 00:00 (UTC) 触发
      │
      ▼
  数据搜集
      │
      ▼
  数据分析
      │
      ▼
  报告生成
      │
      ▼
  GitHub Issue 记录
```

## 🛠️ 使用方法

### 本地运行

```bash
# 安装依赖
pip install -r requirements.txt

# 运行数据搜集
python scrapers/news.py
python scrapers/trends.py

# 运行分析
python analysis/daily_analysis.py

# 生成报告
python reports/generate_report.py
```

### GitHub Actions 自动运行

工作流会在每天早上 8:00 (UTC) 自动运行。

也可以手动触发：
```bash
gh workflow run "每日数据搜集报告"
```

## 📋 输出

### 数据文件
- `news_data.json` - 搜集的新闻数据
- `trends_data.json` - 趋势数据
- `analysis_result.json` - 分析结果

### 报告文件
- `daily_report_YYYY-MM-DD.md` - Markdown 格式报告

### GitHub Artifacts
每次运行后，所有文件会上传为 GitHub Actions Artifacts，可在 Actions 页面下载。

## 🔧 配置

### 修改搜集源

编辑 `scrapers/news.py` 中的 `NEWS_SOURCES` 列表：

```python
NEWS_SOURCES = [
    {
        "name": "你的新闻源",
        "url": "https://example.com/news",
        "selector": "article"
    },
]
```

### 修改搜索关键词

编辑 `scrapers/trends.py` 中的 `CERAMIC_KEYWORDS` 列表：

```python
CERAMIC_KEYWORDS = [
    "你的关键词1",
    "你的关键词2",
]
```

## 📈 未来计划

- [ ] 添加 Instagram 数据爬取
- [ ] 添加竞品价格监控
- [ ] 集成更多新闻源
- [ ] 添加邮件通知
- [ ] 创建数据可视化仪表板

## 📞 联系

- GitHub: https://github.com/jackyecho1029/ceramic-voices-monitoring
- Issues: 提交问题和建议

---

**开始时间**: 2025-02-03
**最后更新**: 2025-02-03
