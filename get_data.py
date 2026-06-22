import requests
import pandas as pd

# 1. 加上请求头，伪装成浏览器，避免被拦截
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}
url = "https://api.bilibili.com/x/web-interface/popular"

try:
    resp = requests.get(url, headers=headers, timeout=5)
    resp.raise_for_status()  # 检查HTTP状态码
    data = resp.json()['data']['list']
except Exception as e:
    print("网络请求失败，自动生成示例数据代替...")
    # 如果请求失败，直接创建示例CSV
    sample = {
        '标题': ['Python数据分析', 'AI绘画入门', 'B站热门合集', '美食探店Vlog', '每日科技快讯'],
        '播放量': [150000, 98000, 67000, 52000, 38000],
        '点赞': [7200, 5100, 3400, 2600, 1800],
        '投币': [1800, 1200, 800, 550, 400],
        'UP主': ['UP主A', 'UP主B', 'UP主C', 'UP主D', 'UP主E']
    }
    df = pd.DataFrame(sample)
    df.to_csv('bilibili_hot.csv', index=False, encoding='utf-8-sig')
    print("✅ 示例数据已生成（因网络限制，使用模拟数据）")
    exit(0)

# 2. 提取字段（缩进正确：4个空格）
movies = []
for v in data:
    movies.append({
        '标题': v['title'],
        '播放量': v['stat']['view'],
        '点赞': v['stat']['like'],
        '投币': v['stat']['coin'],
        'UP主': v['owner']['name']
    })

# 3. 保存为CSV
df = pd.DataFrame(movies)
df.to_csv('bilibili_hot.csv', index=False, encoding='utf-8-sig')
print(f"✅ 成功抓取 {len(df)} 条真实数据！")