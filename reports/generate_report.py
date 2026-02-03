#!/usr/bin/env python3
"""
报告生成脚本
生成 Markdown 格式的每日报告
"""

import json
import os
from datetime import datetime

# 输入输出目录（使用绝对路径）
DATA_DIR = os.path.abspath("../analysis")
OUTPUT_DIR = os.path.abspath("output")
os.makedirs(OUTPUT_DIR, exist_ok=True)

REPORT_TEMPLATE = """# 📊 每日数据搜集报告
日期：{date}

---

## 1. 新闻数据搜集摘要

### 统计
- **总条数**：{news_total}
- **来源数量**：{news_sources_count}

### 按来源统计
{news_by_source}

---

## 2. 趋势分析

### 热门关键词（前5）
{top_trends}

---

## 3. 洞察与建议

### 发现
{insights}

### 下一步行动
- [ ] 根据趋势调整内容策略
- [ ] 关注热门新闻来源
- [ ] 更新竞品监控列表

---

## 4. 数据文件

请查看 GitHub Actions Artifacts 获取完整数据文件。

---

*本报告由自动化系统生成*
*生成时间：{generated_at}
"""

def load_analysis():
    """加载分析结果"""
    analysis_file = os.path.join(DATA_DIR, "analysis_result.json")
    if not os.path.exists(analysis_file):
        return None

    with open(analysis_file, 'r', encoding='utf-8') as f:
        return json.load(f)

def generate_report(analysis_data):
    """生成报告内容"""
    if not analysis_data:
        return "暂无分析数据"

    date = analysis_data.get('date', datetime.now().strftime('%Y-%m-%d'))

    # 处理新闻数据
    news_analysis = analysis_data.get('news', {})
    news_total = news_analysis.get('total', 0)
    news_by_source = news_analysis.get('by_source', {})

    news_by_source_md = ""
    for source, count in news_by_source.items():
        news_by_source_md += f"- **{source}**: {count} 条\n"

    # 处理趋势数据
    trends_analysis = analysis_data.get('trends', {})
    top_trends = trends_analysis.get('top_trends', [])

    top_trends_md = ""
    for i, trend in enumerate(top_trends[:5], 1):
        keyword = trend.get('keyword', '')
        score = trend.get('trend_score', 0)
        top_trends_md += f"{i}. **{keyword}** (热度: {score})\n"

    # 处理洞察
    insights = analysis_data.get('insights', [])
    insights_md = ""
    for insight in insights:
        msg = insight.get('message', '')
        insights_md += f"- {msg}\n"

    # 生成报告
    report = REPORT_TEMPLATE.format(
        date=date,
        news_total=news_total,
        news_sources_count=len(news_by_source),
        news_by_source=news_by_source_md,
        top_trends=top_trends_md,
        insights=insights_md,
        generated_at=datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    )

    return report

def main():
    """主函数"""
    print("正在生成报告...")

    # 加载分析数据
    analysis_data = load_analysis()
    if not analysis_data:
        print("✗ 没有找到分析数据")
        return

    # 生成报告
    report = generate_report(analysis_data)

    # 保存报告
    date_str = datetime.now().strftime('%Y-%m-%d')
    output_file = os.path.join(OUTPUT_DIR, f"daily_report_{date_str}.md")
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(report)

    print(f"✓ 报告已生成: {output_file}")

if __name__ == "__main__":
    main()
