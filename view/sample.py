import streamlit as st
import requests
import pandas as pd

API_ENDPOINT = 'http://127.0.0.1:5000/'

@st.cache_data
def load_data():
    try:
        resp = requests.get(API_ENDPOINT, timeout=5)
        resp.raise_for_status()
        return resp.json()
    except requests.exceptions.RequestException as e:
        st.error(f"API 요청 오류: {e}")
        return []

st.title("FAQ") # FAQ 페이지 제목

faq_data = load_data()
if not faq_data:
    st.info("FAQ 데이터를 불러오지 못했습니다.")
    st.stop()

df = pd.DataFrame(faq_data)

# 기대되는 필드가 question, answer인 경우
for _, row in df.iterrows():
    q = str(row.get("question", "No question"))
    a = str(row.get("answer", "No answer"))
    with st.expander(q):
        st.markdown(a)