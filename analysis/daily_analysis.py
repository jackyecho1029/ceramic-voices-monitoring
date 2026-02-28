#!/usr/bin/env python3
"""
每日数据分析脚本
分析搜集的数据并生成洞察
"""

import json
import os
import pandas as pd
from datetime import datetime

# 输入输出目录（使用绝对路径）
DATA_DIR = os.path.abspath("../scrapers/output")
OUTPUT_DIR = "../reports/output"
os.makedirs(OUTPUT_DIR, exist_ok=True)

def load_data():
    """加载搜集的数据"""
    data = {}

    # 加载新闻数据
    news_file = os.path.join(DATA_DIR, "news_data.json")
    if os.path.exists(news_file):
        with open(news_file, 'r', encoding='utf-8') as f:
            data['news'] = json.load(f)
    else:
        data['news'] = []

    # 加载趋势数据
    trends_file = os.path.join(DATA_DIR, "trends_data.json")
    if os.path.exists(trends_file):
        with open(trends_file, 'r', encoding='utf-8') as f:
            data['trends'] = json.load(f)
    else:
        data['trends'] = []

    return data

def analyze_news(news_data):
    """分析新闻数据"""
    if not news_data:
        return {"total": 0, "by_source": {}}

    # 统计每个来源的新闻数量
    sources = {}
    for item in news_data:
        source = item.get('source', 'Unknown')
        sources[source] = sources.get(source, 0) + 1

    return {
        "total": len(news_data),
        "by_source": sources
    }

def analyze_trends(trends_data):
    """分析趋势数据"""
    if not trends_data:
        return {"total": 0, "top_trends": []}

    # 找出趋势分数最高的关键词
    sorted_trends = sorted(trends_data, key=lambda x: x.get('trend_score', 0), reverse=True)

    return {
        "total": len(trends_data),
        "top_trends": sorted_trends[:5]
    }

def main():
    """主函数"""
    print("正在分析数据...")

    # 加载数据
    data = load_data()

    # 分析
    news_analysis = analyze_news(data.get('news', []))
    trends_analysis = analyze_trends(data.get('trends', []))

    # 保存分析结果
    analysis_result = {
        "date": datetime.now().isoformat(),
        "news": news_analysis,
        "trends": trends_analysis,
        "insights": generate_insights(news_analysis, trends_analysis)
    }

    output_file = os.path.join(OUTPUT_DIR, "analysis_result.json")
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(analysis_result, f, ensure_ascii=False, indent=2)

    print(f"✓ 分析完成，已保存到 {output_file}")

def generate_insights(news_analysis, trends_analysis):
    """生成洞察"""
    insights = []

    # 基于新闻数量的洞察
    if news_analysis.get('total', 0) > 0:
        insights.append({
            "type": "news_volume",
            "message": f"今日搜集了 {news_analysis.get('total')} 条行业新闻"
        })

    # 基于趋势的洞察
    top_trends = trends_analysis.get('top_trends', [])
    if top_trends:
        top_keyword = top_trends[0].get('keyword', '')
        insights.append({
            "type": "trend",
            "message": f"最高热度关键词: {top_keyword}"
        })

    return insights

if __name__ == "__main__":
    main()
