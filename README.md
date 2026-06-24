# 📊 B站热门视频自动化数据分析看板

基于 Python + Streamlit + GitHub Actions 构建的自动化数据监控系统，每日自动抓取B站热门榜单，实现数据可视化与趋势追踪。

## ✨ 核心功能
- 🕷️ **自动化爬虫**：每日定时抓取B站热门视频数据（GitHub Actions调度）
- 💾 **历史存储**：SQLite 数据库持久化存储，支持历史趋势分析
- 📈 **可视化看板**：核心指标监控、TOP10排行、播放量趋势图、互动率分析
- 🎛️ **交互筛选**：支持按UP主筛选数据，一键导出CSV

## 🛠️ 技术栈
- **后端**：Python (Requests, Pandas)
- **可视化**：Streamlit, Matplotlib
- **数据库**：SQLite
- **调度**：GitHub Actions (Cron定时任务)
- **部署**：Streamlit Cloud

## 🚀 在线体验
[点击查看在线看板](https://bilibili-dashboard-95jbpyewcaxybbr4d6wehu.streamlit.app/)

## 📦 本地运行
1. 克隆仓库：`git clone https://github.com/Let-07/bilibili-dashboard.git`
2. 安装依赖：`pip install -r requirements.txt`
3. 运行看板：`streamlit run app.py`