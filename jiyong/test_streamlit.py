import streamlit as st
import requests
import pandas as pd

API_URL = "http://127.0.0.1:5000/scrapyards"

st.title("🏭 수도권 폐차장 데이터 조회")

# 🧭 필터 입력
region = st.text_input("지역 코드 입력 (예: 02=서울, 01=경기, 11=인천)", "")
subregion = st.text_input("시군구 입력 (예: 금천구, 부천시 등)", "")

# 🚀 버튼 클릭 시 Flask에 요청
if st.button("폐차장 데이터 불러오기"):
    try:
        params = {}
        if region:
            params["region"] = region
        if subregion:
            params["subregion"] = subregion

        # GET 요청으로 Flask에서 JSON 데이터 받기
        resp = requests.get(API_URL, params=params, timeout=5)
        resp.raise_for_status()

        data = resp.json()
        if not data:
            st.warning("⚠️ 조건에 맞는 폐차장 데이터가 없습니다.")
        else:
            st.success(f"✅ {len(data)}개의 데이터를 불러왔습니다.")
            df = pd.DataFrame(data)
            st.dataframe(df, use_container_width=True)

    except requests.exceptions.RequestException as e:
        st.error(f"❌ Flask 서버 연결 실패: {e}")
