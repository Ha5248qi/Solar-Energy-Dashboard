import streamlit as st
import pandas as pd
import plotly.express as px
from utils.data_loader import load_data 

# 页面标题配置
st.set_page_config(
    page_title="Global Solar Advisor",
    page_icon="☀️",
    layout="wide"  # 设为宽屏模式
)

st.title("☀️ Global Solar Adviso")

try:
    df = load_data("../data/solar_energy_worldwide.csv")
    st.sidebar.header("🔍 filter bar")
    all_regions = df['Region'].unique()
    # 创建多选框
    selected_regions = st.sidebar.multiselect(
        "(Choose Region):",
        options=all_regions,
        default=all_regions 
    )
    
    # 根据用户选择过滤数据
    if selected_regions:
        df = df[df['Region'].isin(selected_regions)]
    else:
        st.warning("Choose at least one region!")
        st.stop() 

    
    # 展示关键指标 (Metrics)
    col1, col2, col3 = st.columns(3)
    col1.metric("🌍 Cities Covered", len(df))
    col2.metric("💰 Return on Investment (ROI)", f"{df['ROI_Percentage'].mean():.2f}%")
    col3.metric("💡 Highest Viability Score", df['Solar_Viability_Score'].max())

    #插入地图
    st.markdown("---") # 分割线
    st.subheader("🗺️ Global Solar PV Potential Map")

    # 使用 Plotly 绘制地图
    # lat/lon: 经纬度数据列名
    # size: 气泡大小代表回报率 (ROI)
    # color: 颜色深浅代表可行性评分 (Score)
    map_fig = px.scatter_mapbox(
        df,
        lat="Latitude",
        lon="Longitude",
        hover_name="City",
        size="ROI_Percentage",
        color="Solar_Viability_Score",
        color_continuous_scale="RdYlGn",  # 红-黄-绿 配色
        size_max=15,                      # 气泡最大尺寸
        zoom=1,                           # 初始缩放层级 (1=全球视角)
        mapbox_style="open-street-map"    # 地图底图样式
    )
    
    st.plotly_chart(map_fig, use_container_width=True)
    # 展示数据表
    st.subheader("Data Overview")
    st.dataframe(df)

except FileNotFoundError:
    st.error("❌ 找不到文件！请检查 data 文件夹里有没有 csv 文件。")
except Exception as e:
    st.error(f"❌ 发生错误: {e}")