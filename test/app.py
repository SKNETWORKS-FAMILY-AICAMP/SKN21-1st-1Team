"""
Author: 박수빈
Date: 2025-10-22
Description: 검색 후 선택된 업체만 지도에 표시 테스트
"""

import streamlit as st
import pandas as pd
import requests
import pydeck as pdk
import re
import time

KAKAO_API_KEY = "9cffe66368178b182f1961dfc94b120e"

# -----------------------------
# 주소 → 좌표 변환
# -----------------------------
def get_lat_lon(address: str):
    clean_address = re.sub(r"[()]", "", address).strip()
    try:
        url = "https://dapi.kakao.com/v2/local/search/address.json"
        headers = {"Authorization": f"KakaoAK {KAKAO_API_KEY}"}
        params = {"query": clean_address}
        res = requests.get(url, headers=headers, params=params)
        result = res.json()
        if result.get('documents'):
            lat = float(result['documents'][0]['y'])
            lon = float(result['documents'][0]['x'])
            return lat, lon
        else:
            return None, None
    except Exception as e:
        st.error(f"주소 변환 오류: {e}")
        return None, None

# -----------------------------
# CSV 데이터 로드
# -----------------------------
@st.cache_data
def load_data():
    df = pd.read_csv("scrap_yard_data.csv", encoding="utf-8-sig")
    return df

# -----------------------------
# Streamlit UI
# -----------------------------
st.title("🚗 폐차장 위치 검색 후 선택 표시")

df = load_data()

# 지역 필터
df['지역'] = df['주소'].str.extract(r'(서울|부산|대전|대구|광주|인천|울산|세종|경기|강원|충북|충남|전북|전남|경북|경남|제주)')
regions = ["전체"] + sorted(df["지역"].dropna().unique().tolist())
selected_region = st.selectbox("지역 선택", regions)

# 업체명 검색
search_name = st.text_input("업체명 검색 (부분 입력 가능)", "").strip()

# -----------------------------
# 필터링
# -----------------------------
filtered = df.copy()
if selected_region != "전체":
    filtered = filtered[filtered["지역"] == selected_region]
if search_name:
    filtered = filtered[filtered["업체명"].str.contains(search_name, case=False, na=False)]

st.subheader(f"🔍 조회 결과 ({len(filtered)}건)")

# 조회된 업체 목록 출력
st.dataframe(filtered[['업체명','담당자','주소','전화번호']])

# -----------------------------
# 업체 선택
# -----------------------------
if not filtered.empty:
    selected_name = st.selectbox("지도에 표시할 업체 선택", filtered['업체명'].tolist())

    selected_row = filtered[filtered['업체명'] == selected_name].iloc[0]
    lat, lon = get_lat_lon(selected_row["주소"])
    if lat is not None and lon is not None:
        layer = pdk.Layer(
            "ScatterplotLayer",
            data=[{
                "업체명": selected_row["업체명"],
                "담당자": selected_row["담당자"],
                "주소": selected_row["주소"],
                "전화번호": selected_row["전화번호"],
                "latitude": lat,
                "longitude": lon
            }],
            get_position='[longitude, latitude]',
            get_color='[255, 100, 0, 200]',
            get_radius=300,
            pickable=True
        )
        view_state = pdk.ViewState(
            latitude=lat,
            longitude=lon,
            zoom=14
        )
        st.pydeck_chart(pdk.Deck(
            layers=[layer],
            initial_view_state=view_state,
            tooltip={"text": "{업체명}\n{담당자}\n{주소}\n{전화번호}"}
        ))
    else:
        st.warning("선택한 업체의 좌표를 가져올 수 없습니다.")
