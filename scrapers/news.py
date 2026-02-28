#!/usr/bin/env python3
"""
陶瓷行业新闻数据搜集脚本
搜集来自主要网站的行业新闻和趋势
"""

import requests
from bs4 import BeautifulSoup
import json
from datetime import datetime
import os

# 输出目录（使用相对于脚本的路径）
OUTPUT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "output")
os.makedirs(OUTPUT_DIR, exist_ok=True)

# 新闻源列表（使用稳定可靠的源）
NEWS_SOURCES = [
    {
        "name": "Etsy Blog",
        "url": "https://blog.etsy.com",
        "selector": "article",
        "description": "Etsy 官方博客"
    },
    {
        "name": "Etsy Seller Handbook",
        "url": "https://www.etsy.com/blog/seller-news",
        "selector": "article",
        "description": "卖家手册和新闻"
    },
    {
        "name": "Crafts Magazine",
        "url": "https://craftsmag.com",
        "selector": "article",
        "description": "手工艺杂志"
    }
]

def fetch_news(source):
    """获取单个新闻源的内容"""
    try:
        response = requests.get(source["url"], timeout=10)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, 'html.parser')

        articles = []
        items = soup.select(source["selector"])

        for item in items[:5]:  # 每个源最多取5条
            title = item.find(['h1', 'h2', 'h3', 'h4'])
            link = item.find('a')

            if title and link:
                articles.append({
                    "source": source["name"],
                    "title": title.get_text(strip=True),
                    "url": link.get('href'),
                    "date": datetime.now().isoformat()
                })

        return articles

    except Exception as e:
        print(f"获取 {source['name']} 失败: {e}")
        return []

def main():
    """主函数"""
    all_news = []

    for source in NEWS_SOURCES:
        print(f"正在获取: {source['name']}")
        articles = fetch_news(source)
        all_news.extend(articles)

    # 保存到 JSON 文件
    output_file = os.path.join(OUTPUT_DIR, "news_data.json")
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(all_news, f, ensure_ascii=False, indent=2)

    print(f"✓ 已搜集 {len(all_news)} 条新闻")
    print(f"✓ 已保存到 {output_file}")

if __name__ == "__main__":
    main()
