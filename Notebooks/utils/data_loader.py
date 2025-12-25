import pandas as pd
import streamlit as st

@st.cache_data#缓存功能
def load_data(filepath):
    """
    读取并清洗数据
    """
    df = pd.read_csv(filepath)

    if df['ROI_Percentage'].dtype == 'object':
        df['ROI_Percentage'] = df['ROI_Percentage'].str.replace('%', '').astype(float)
    # 按照 ROI从高到低排序
    df = df.sort_values(by='ROI_Percentage', ascending=False)
    
    return df