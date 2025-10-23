"""
Author      : 신지용
Date        : 2025-10-22
Last Update : 2025-10-23
Description : Streamlit UI를 통해 Flask API 결과를 시각화하는 테스트 페이지
File Role   : API 호출 및 데이터프레임 출력용 간단 UI
"""

import streamlit as st
import pandas as pd
import requests

st.set_page_config(page_title="🚗 Flask 연동 테스트", layout="wide")
st.title("🚗 Flask → Streamlit 연동 테스트")

# Flask 서버 주소
url = "http://127.0.0.1:5000/scrapyards"

# 버튼 클릭 시 Flask API 호출
if st.button("데이터 불러오기"):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            st.success(f"✅ {len(data)}개의 데이터를 불러왔습니다.")
            df = pd.DataFrame(data)
            st.dataframe(df, use_container_width=True)
        else:
            st.error(f"서버 응답 오류: {response.status_code}")
    except Exception as e:
        st.error(f"❌ Flask 서버 연결 실패: {e}")
