import streamlit as st
import pandas as pd
import yfinance as yf

st.set_page_config(page_title="בדיקת דאשבורד", page_icon="📊", layout="wide")

# כיוון עברית
st.markdown("""<style>h1, h2, h3, p, span { text-align: right; direction: RTL; }</style>""", unsafe_allowed_allow_html=True)

st.title("📊 דאשבורד עוגני משכנתא - בדיקת חיבור")
st.write("---")

# נתוני פריים בסיסיים
prime_rate = 3.75 + 1.5
st.metric(label="ריבית הפריים הנוכחית (Prime)", value=f"{prime_rate:.2f}%")

st.write("---")
st.write("אם אתה רואה את המסך הזה, השרת באוויר והכל עובד פיקס! נתחיל להחזיר את הגרפים בהדרגה.")
