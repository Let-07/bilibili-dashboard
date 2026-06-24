import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import db_utils
import os
from pathlib import Path

st.set_page_config(layout="wide")
st.title("📊 B站热门视频分析 (自动化数据管道)")

@st.cache_data(ttl=600)
def load_data_from_db():
    return db_utils.load_recent_data(days=7)

df = load_data_from_db()

if not df.empty:
    latest_date = df['date'].max()
    st.caption(f"🔄 数据最后更新：{latest_date} ｜ 共 {len(df)} 条记录")

if not df.empty:
    # 计算互动率：(点赞+投币) / 播放量 * 100，保留2位小数
    df['互动率(%)'] = ((df['likes'] + df['coins']) / df['views'] * 100).round(2)

if df.empty:
    st.warning("⏳ 数据库暂无数据，请等待定时抓取任务执行。")
    st.stop()

col1, col2, col3 = st.columns(3)
col1.metric("📹 近7天视频数", len(df))
col2.metric("📊 平均播放量", f"{df['views'].mean():,.0f}")
col3.metric("🔥 最高播放量", f"{df['views'].max():,}")

st.sidebar.header("🎛️ 控制面板")
author_list = ['全部'] + df['author'].unique().tolist()
selected_author = st.sidebar.selectbox("筛选UP主", author_list)
if selected_author != '全部':
    df = df[df['author'] == selected_author]

st.dataframe(df[['date', 'title', 'views', 'likes', 'coins', '互动率(%)', 'author']])

st.subheader("📊 播放量 TOP 10")
top10 = df.sort_values('views', ascending=False).head(10)
st.bar_chart(top10.set_index('title')['views'])

if 'date' in df.columns:
    st.subheader("📈 每日总播放量趋势")
    daily_trend = df.groupby('date')['views'].sum().reset_index()
    daily_trend = daily_trend.sort_values('date')
    st.line_chart(daily_trend.set_index('date'))

st.subheader("📈 播放量与点赞关系")
fig, ax = plt.subplots()
ax.scatter(df['views'], df['likes'], alpha=0.6, color='#FF6B6B')
ax.set_xlabel('播放量')
ax.set_ylabel('点赞')
st.pyplot(fig)

@st.cache_data
def convert_df(df):
    return df.to_csv(index=False).encode('utf-8-sig')

csv = convert_df(df)
st.download_button("📥 下载当前筛选数据", data=csv, file_name='bilibili_filtered.csv', mime='text/csv')
with st.expander("📋 查看系统运行日志"):
    log_path = Path("logs") / "scraper.log"
    if log_path.exists():
        try:
            with open(log_path, 'r', encoding='gbk') as f:
                lines = f.readlines()
            st.code(''.join(lines[-20:]), language='log')
        except UnicodeDecodeError:
            # 如果 gbk 也不行，尝试其他编码或使用错误处理
            with open(log_path, 'r', encoding='utf-8', errors='ignore') as f:
                lines = f.readlines()
            st.code(''.join(lines[-20:]), language='log')
    else:
        st.info("暂无日志记录")
st.sidebar.caption(f"📦 数据来源: SQLite | 共 {len(load_data_from_db())} 条记录")