import streamlit as st

st.set_page_config(page_title="עוגני משכנתא", page_icon="📊")

# עיצוב בסיסי לעברית וישור לימין
st.markdown("""
    <style>
    h1, h2, h3, p, div, span { text-align: right; direction: RTL; }
    div[data-testid="stMetricValue"] { text-align: right; direction: RTL; }
    </style>
""", unsafe_allowed_allow_html=True)

st.title("📊 דאשבורד עוגני משכנתא - בדיקה סופית")
st.write("---")

# נתוני פריים (קבוע מאי 2026: 3.75% + 1.5%)
prime_rate = 5.25

col1, col2 = st.columns(2)
with col1:
    st.metric(label="ריבית הפריים (Prime)", value=f"{prime_rate:.2f}%")
with col2:
    st.metric(label="בנק ישראל (עוגן)", value="3.75%")

st.write("---")
st.success("אם אתה רואה את זה - הצינור נקי ועובד! מכאן נוכל להחזיר רק את מה שצריך.")
