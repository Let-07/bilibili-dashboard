import sqlite3
import pandas as pd
from datetime import datetime, timedelta

DB_PATH = "bilibili.db"

def get_connection():
    """获取数据库连接"""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    """初始化数据表（如果不存在）"""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS video_data (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT NOT NULL,
            title TEXT NOT NULL,
            views INTEGER,
            likes INTEGER,
            coins INTEGER,
            author TEXT,
            UNIQUE(date, title)
        )
    """)
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_date ON video_data(date)")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_author ON video_data(author)")
    conn.commit()
    conn.close()
    print("✅ 数据库初始化完成（bilibili.db）")

def save_data(df_new):
    """批量插入或更新数据"""
    conn = get_connection()
    cursor = conn.cursor()
    inserted = 0
    for _, row in df_new.iterrows():
        try:
            cursor.execute("""
                INSERT OR REPLACE INTO video_data (date, title, views, likes, coins, author)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (row['日期'], row['标题'], row['播放量'], row['点赞'], row['投币'], row['UP主']))
            inserted += 1
        except Exception as e:
            print(f"⚠️ 插入失败: {row['标题']} - {e}")
    conn.commit()
    conn.close()
    print(f"✅ 成功写入 {inserted} 条数据到数据库")

def load_all_data():
    """加载全部历史数据"""
    conn = get_connection()
    df = pd.read_sql("SELECT * FROM video_data ORDER BY date DESC, views DESC", conn)
    conn.close()
    return df

def load_recent_data(days=7):
    """仅加载最近N天的数据（看板专用）"""
    conn = get_connection()
    cutoff = (datetime.now() - timedelta(days=days)).strftime("%Y-%m-%d")
    df = pd.read_sql(f"SELECT * FROM video_data WHERE date >= '{cutoff}' ORDER BY date DESC", conn)
    conn.close()
    return df

if __name__ == "__main__":
    init_db()