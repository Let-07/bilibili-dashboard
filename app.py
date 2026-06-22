import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.title("📊 B站热门视频分析")
df = pd.read_csv('bilibili_hot.csv')

# 显示表格
st.dataframe(df)

# 画个柱状图（按播放量排序）
top10 = df.sort_values('播放量', ascending=False).head(10)
st.bar_chart(top10.set_index('标题')['播放量'])
# 显示关键指标卡片
col1, col2, col3 = st.columns(3)
col1.metric("总视频数", len(df))
col2.metric("平均播放量", f"{df['播放量'].mean():,.0f}")
col3.metric("最高播放量", f"{df['播放量'].max():,}")

# 加一个UP主筛选器
author = st.selectbox("筛选UP主", df['UP主'].unique())
st.dataframe(df[df['UP主'] == author])

plt.rcParams['font.sans-serif'] = ['SimHei', 'Microsoft YaHei', 'PingFang SC']  # 指定中文字体
plt.rcParams['axes.unicode_minus'] = False  # 解决负号 '-' 显示为方块的问题
st.subheader("📈 播放量与点赞关系")
fig, ax = plt.subplots()
ax.scatter(df['播放量'], df['点赞'], alpha=0.6)
ax.set_xlabel('播放量')
ax.set_ylabel('点赞')
st.pyplot(fig)

@st.cache_data
def convert_df(df):
    return df.to_csv(index=False).encode('utf-8-sig')

csv = convert_df(df)
st.download_button("📥 下载当前数据", data=csv, file_name='bilibili_data.csv', mime='text/csv')
