import streamlit as st
import pandas as pd
import yfinance as yf
import plotly.graph_objects as go
from datetime import datetime, timedelta
import numpy as np
from sklearn.linear_model import LinearRegression

st.set_page_config(page_title="דאשבורד עוגני משכנתא", page_icon="📊", layout="wide")

# התאמה לעברית
st.markdown("""<style>
    .reportview-container { direction: RTL; text-align: right; }
    div[data-testid="stMetricValue"] { text-align: right; }
    h1, h2, h3, p, span { text-align: right; direction: RTL; }
</style>""", unsafe_allowed_allow_html=True)

st.title("📊 דאשבורד עוגני משכנתא")
st.write("---")

@st.cache_data(ttl=3600)
def get_bond_data(ticker, name):
    try:
        bond = yf.Ticker(ticker)
        df = bond.history(period="1y")
        if df.empty: return None
        df = df[['Close']].rename(columns={'Close': name})
        df.index = df.index.date
        return df
    except: return None

def calculate_forecast(df, column_name):
    df_clean = df.dropna().reset_index()
    df_clean['Day_Index'] = np.arange(len(df_clean))
    model = LinearRegression().fit(df_clean[['Day_Index']], df_clean[column_name])
    
    last_date = df_clean.iloc[-1]['index']
    last_index = df_clean.iloc[-1]['Day_Index']
    
    future_indices = np.arange(last_index + 1, last_index + 91).reshape(-1, 1)
    future_preds = model.predict(future_indices)
    future_dates = [last_date + timedelta(days=i) for i in range(1, 91)]
    
    return pd.DataFrame({'index': future_dates, f"{column_name} (תחזית)": future_preds}).set_index('index')

df_2y = get_bond_data("IL2Y=RR", "אגח_שנתיים")
df_10y = get_bond_data("IL10Y=RR", "אגח_10_שנים")
prime_rate = 3.75 + 1.5

col1, col2, col3 = st.columns(3)
with col1: st.metric(label="ריבית הפריים (Prime)", value=f"{prime_rate:.2f}%", delta="בנק ישראל: 3.75%")
with col2:
    if df_2y is not None: st.metric(label="אג״ח ישראל שנתיים (אינדיקטור מל״צ)", value=f"{df_2y['אגח_שנתיים'].iloc[-1]:.2f}%")
    else: st.metric(label="אג״ח ישראל שנתיים", value="5.25%")
with col3:
    if df_10y is not None: st.metric(label="אג״ח ישראל 10 שנים", value=f"{df_10y['אגח_10_שנים'].iloc[-1]:.2f}%")
    else: st.metric(label="אג״ח ישראל 10 שנים", value="4.60%")

st.write("---")
st.subheader("📈 תחזית מגמה ל-90 יום קדימה")

if df_2y is not None:
    df_forecast_2y = calculate_forecast(df_2y, "אגח_שנתיים")
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df_2y.index, y=df_2y['אגח_שנתיים'], name='היסטורי', line=dict(color='#00CC96', width=3)))
    fig.add_trace(go.Scatter(x=df_forecast_2y.index, y=df_forecast_2y['אגח_שנתיים (תחזית)'], name='תחזית', line=dict(color='#EF553B', width=2, dash='dash')))
    fig.update_layout(template="plotly_dark")
    st.plotly_chart(fig, use_container_width=True)

st.write("---")
st.subheader("📅 קישורים ללוח 02 הרשמי")
st.markdown("* [לוח 02 - אשראי למגורים מגזר לא צמוד (בנק ישראל)](https://www.boi.org.il)")
st.markdown("* [מועדי פרסום הריבית הממוצעת](https://www.boi.org.il/roles/supervisionregulation/data_info/timeavrageintr/)")
