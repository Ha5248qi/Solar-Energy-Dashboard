import pandas as pd
import streamlit as st

# @st.cache_data 是 Streamlit 的“超级缓存”功能
# 意思：如果数据读过一次，就存到内存里，下次不要重新读文件了（速度变快10倍）
@st.cache_data
def load_data(filepath):
    """
    读取并清洗数据
    """
    # 1. 读取 CSV
    df = pd.read_csv(filepath)
    
    # 2. 清洗数据：处理 ROI_Percentage 里的 '%' 号
    # 检查一下是不是字符类型，如果是，去掉 % 并转为数字
    
    if df['ROI_Percentage'].dtype == 'object':
        df['ROI_Percentage'] = df['ROI_Percentage'].str.replace('%', '').astype(float)
    # 3. 按照 ROI (投资回报率) 从高到低排序，这样好城市排前面
    df = df.sort_values(by='ROI_Percentage', ascending=False)
    
    return df