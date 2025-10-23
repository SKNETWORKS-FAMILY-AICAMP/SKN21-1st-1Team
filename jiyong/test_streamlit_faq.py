"""
Author      : 신지용
Date        : 2025-10-23
Description : Streamlit UI를 통해 Flask API의 폐차장 + FAQ 데이터를 시각화
File Role   : Flask API 호출 및 데이터프레임 출력용 통합 UI
"""

import streamlit as st
import pandas as pd
import requests

st.set_page_config(page_title="🚗 폐차장 & FAQ 통합 대시보드", layout="wide")
st.title("🚗 수도권 폐차장 & FAQ 통합 데이터 조회")

# Flask 서버 주소
SCRAPYARD_URL = "http://127.0.0.1:5000/scrapyards"
FAQ_URL = "http://127.0.0.1:5000/faqs"

# 탭 구성
tab1, tab2 = st.tabs(["🏭 폐차장 데이터", "💬 FAQ 데이터"])

# ------------------------------
# 🚗 폐차장 탭
# ------------------------------
with tab1:
    st.subheader("🏭 폐차장 데이터 조회")

    # 필터 옵션
    region = st.text_input("지역 코드 입력 (예: 02, 01, 11)", "")
    subregion = st.text_input("시군구 입력 (예: 금천구, 부천시 등)", "")

    # 버튼 클릭 시 데이터 요청
    if st.button("폐차장 데이터 불러오기"):
        try:
            params = {}
            if region:
                params["region"] = region
            if subregion:
                params["subregion"] = subregion

            response = requests.get(SCRAPYARD_URL, params=params)
            if response.status_code == 200:
                data = response.json()
                if len(data) > 0:
                    st.success(f"✅ {len(data)}개의 폐차장 데이터를 불러왔습니다.")
                    st.dataframe(pd.DataFrame(data), use_container_width=True)
                else:
                    st.warning("⚠️ 해당 조건에 맞는 데이터가 없습니다.")
            else:
                st.error(f"서버 오류 발생: {response.status_code}")
        except Exception as e:
            st.error(f"❌ Flask 서버 연결 실패: {e}")

# ------------------------------
# 💬 FAQ 탭
# ------------------------------
with tab2:
    st.subheader("💬 FAQ 데이터 조회")

    if st.button("FAQ 데이터 불러오기"):
        try:
            response = requests.get(FAQ_URL)
            if response.status_code == 200:
                data = response.json()
                if len(data) > 0:
                    st.success(f"✅ {len(data)}개의 FAQ 데이터를 불러왔습니다.")
                    df = pd.DataFrame(data)
                    st.dataframe(df, use_container_width=True)
                else:
                    st.warning("⚠️ FAQ 데이터가 없습니다.")
            else:
                st.error(f"서버 오류 발생: {response.status_code}")
        except Exception as e:
            st.error(f"❌ Flask 서버 연결 실패: {e}")
