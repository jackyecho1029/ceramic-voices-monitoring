#!/usr/bin/env python3
"""
Instagram 竞品数据搜集脚本
公开收集Instagram账号的内容数据（无需登录）
"""

import requests
import json
from datetime import datetime
import os
from bs4 import BeautifulSoup

# 输出目录（使用相对于脚本的路径）
OUTPUT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "output")
os.makedirs(OUTPUT_DIR, exist_ok=True)

# 竞品账号列表
COMPETITORS = [
    {
        "username": "heathceramics",
        "name": "Heath Ceramics",
        "description": "现代建筑陶瓷"
    },
    {
        "username": "keramicstudio",
        "name": "Keramic Studio",
        "description": "温暖手作陶瓷"
    },
    {
        "username": "juliettemcinty",
        "name": "Juliette McInty",
        "description": "自然有机陶瓷"
    },
    {
        "username": "thecupcollection",
        "name": "The Cup Collection",
        "description": "杯具专门店"
    }
]

def get_instagram_data(username):
    """
    公开获取Instagram账号数据
    注意：Instagram 需要登录才能获取完整数据，这里使用公开数据
    """
    try:
        # 尝试访问Instagram页面
        url = f"https://www.instagram.com/{username}/"
        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
        }
        response = requests.get(url, headers=headers, timeout=10)

        # 如果需要登录，返回基本信息
        if "login" in response.url or response.status_code == 404:
            return {
                "username": username,
                "status": "login_required",
                "note": "此账号需要登录才能查看，建议使用 Instaloader 等工具",
                "timestamp": datetime.now().isoformat()
            }

        # 解析页面内容
        soup = BeautifulSoup(response.text, 'html.parser')

        # 尝试提取基本信息
        meta_description = soup.find('meta', property='og:description')
        meta_image = soup.find('meta', property='og:image')
        meta_title = soup.find('meta', property='og:title')

        return {
            "username": username,
            "title": meta_title.get('content', '') if meta_title else '',
            "description": meta_description.get('content', '') if meta_description else '',
            "image": meta_image.get('content', '') if meta_image else '',
            "status": "success",
            "timestamp": datetime.now().isoformat()
        }

    except Exception as e:
        return {
            "username": username,
            "status": "error",
            "error": str(e),
            "timestamp": datetime.now().isoformat()
        }

def analyze_competitor_data(data):
    """分析竞品数据并生成洞察"""
    insights = []

    # 统计成功获取的账号
    success_count = sum(1 for item in data if item.get('status') == 'success')
    insights.append({
        "type": "success_rate",
        "message": f"成功获取 {success_count}/{len(data)} 个竞品账号的公开数据"
    })

    # 识别需要登录的账号
    login_required = [item for item in data if item.get('status') == 'login_required']
    if login_required:
        insights.append({
            "type": "login_required",
            "message": f"以下账号需要登录才能查看完整数据：{', '.join([item['username'] for item in login_required])}"
        })
        insights.append({
            "type": "recommendation",
            "message": "建议使用 Instaloader 等专业工具进行深度数据收集"
        })

    return insights

def main():
    """主函数"""
    print("=" * 50)
    print("开始搜集 Instagram 竞品数据")
    print("=" * 50)

    all_data = []

    for competitor in COMPETITORS:
        username = competitor['username']
        name = competitor['name']
        print(f"\n正在获取: {name} (@{username})")

        data = get_instagram_data(username)
        data['competitor_name'] = name
        data['competitor_description'] = competitor['description']
        all_data.append(data)

        status = data.get('status', 'unknown')
        if status == 'success':
            print(f"  ✓ 成功获取数据")
        elif status == 'login_required':
            print(f"  ⚠️  需要登录才能查看完整数据")
        else:
            print(f"  ✗ 获取失败: {data.get('error', 'Unknown error')}")

    # 保存数据
    output_file = os.path.join(OUTPUT_DIR, "instagram_data.json")
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(all_data, f, ensure_ascii=False, indent=2)

    print("\n" + "=" * 50)
    print(f"✓ 已保存数据到: {output_file}")

    # 生成洞察
    insights = analyze_competitor_data(all_data)

    # 保存洞察
    insights_file = os.path.join(OUTPUT_DIR, "instagram_insights.json")
    with open(insights_file, 'w', encoding='utf-8') as f:
        json.dump(insights, f, ensure_ascii=False, indent=2)

    print(f"✓ 已保存洞察到: {insights_file}")
    print("\n" + "=" * 50)
    print("建议:")
    print("=" * 50)

    for insight in insights:
        print(f"\n• {insight['message']}")

    print("\n" + "=" * 50)
    print("下一步行动:")
    print("=" * 50)
    print("""
1. 考虑安装 Instaloader 进行深度数据收集
   pip install instaloader

2. 研究竞品的内容策略
   - 观察发布频率
   - 分析热门内容类型
   - 研究互动策略

3. 优化 Ceramic Voices 的差异化定位
   - 基于 Instagram 数据优化视觉风格
   - 调整内容发布时间
   - 参考竞品的 Hashtag 策略
    """)

if __name__ == "__main__":
    main()
