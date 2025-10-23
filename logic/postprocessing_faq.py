"""
Author: 최주원
Date: 2025-10-23
Description: 폐차장 faq 조회 Data 후처리 프로그램
"""

# 화면에 조건에 따른 출력을 위한 Data Select SQL 필요.
import streamlit as st
import requests
import json
import pandas as pd

# Flask API 엔드포인트
API_ENDPOINT = 'http://127.0.0.1:5000/'  # Flask 앱이 실행되는 주소

# API로부터 FAQ 데이터를 가져오는 함수
@st.cache_data  # 데이터 캐싱
def load_data():
    try:
        response = requests.get(API_ENDPOINT)
        response.raise_for_status()  # HTTP 오류 발생 시 예외 발생
        data = response.json()
        return data
    except requests.exceptions.RequestException as e:
        st.error(f"API 요청 오류: {e}")
        return None

# Streamlit 앱
st.title("FAQ 데이터")

# FAQ 데이터 가져오기
faq_data = load_data()

if faq_data:
    # 데이터프레임으로 변환
    df = pd.DataFrame(faq_data)

    # 컬럼 순서 변경 (id, question, answer 순서로)
    if 'id' in df.columns and 'question' in df.columns and 'answer' in df.columns:
        df = df[['id', 'question', 'answer']]

    # Streamlit 데이터 테이블에 표시
    st.dataframe(df, use_container_width=True)
else:
    st.write("FAQ 데이터를 불러오지 못했습니다.")