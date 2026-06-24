import requests
import pandas as pd
import datetime
import db_utils
import logging

logging.basicConfig(filename='scraper.log', level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')


def fetch_and_save():
    today = datetime.datetime.now().strftime("%Y-%m-%d")
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}
    url = "https://api.bilibili.com/x/web-interface/popular"

    try:
        resp = requests.get(url, headers=headers, timeout=5)
        data = resp.json()['data']['list']
        movies = []
        for v in data:
            movies.append({
                '日期': today,
                '标题': v['title'],
                '播放量': v['stat']['view'],
                '点赞': v['stat']['like'],
                '投币': v['stat']['coin'],
                'UP主': v['owner']['name']
            })
        df_new = pd.DataFrame(movies)
        db_utils.init_db()
        db_utils.save_data(df_new)
        total = len(db_utils.load_all_data())
        logging.info(f"✅ {today} 数据入库成功，当前共 {total} 条历史记录")
    except Exception as e:
        logging.error(f"❌ 抓取失败: {e}")
        db_utils.init_db()
        if len(db_utils.load_all_data()) == 0:
            sample = pd.DataFrame({
                '日期': [today], '标题': ['等待首次数据抓取'],
                '播放量': [0], '点赞': [0], '投币': [0], 'UP主': ['系统']
            })
            db_utils.save_data(sample)


if __name__ == "__main__":
    fetch_and_save()