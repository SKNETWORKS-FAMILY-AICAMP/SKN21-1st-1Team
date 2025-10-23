"""
Author: 문지영
Date: 2025-10-22
Description: 폐차장 위치 검색 화면
"""

# Data 화면 출력을 위한 streamlit 코드 작성.
# TODO 지영님 Streamlit 활용하여 화면 작성 필요.

import streamlit as st
import pandas as pd

# 1. 페이지 설정
st.set_page_config(
    page_title="수도권 폐차장 조회 및 FAQ 시스템",
    page_icon="🚙",
    layout="wide",
    initial_sidebar_state="expanded"
)


# 2. 사이드바 메뉴 구현
st.sidebar.title("🛠️ 시스템 메뉴")
menu = st.sidebar.radio(
    " 원하는 서비스를 선택하세요: ",
    ('폐차장 조회', 'FAQ 검색 시스템', '통계 시각화', 'SQL 질의 진행')
)


# 3. 메인 콘텐츠 함수 정의
def show_scrapyard_finder():
    """ 폐차장 조회 페이지 """
    st.header ("📍수도권 폐차장 조회")
    st.write("지역 또는 업체명으로 등록된 폐차장 정보를 검색하세요.")

    col1, col2 = st.columns(2)

    with col1:
        selected_area = st.selectbox(
            "지역별 검색",
            ['전체', '서울', '경기', '인천'],
            index = 0   # 기본값 '전체'
        )
    with col2:
        search_name = st.text_input("업체명 검색 (키워드)", max_chars=50)





# 4. 메인 라우팅 (메뉴에 따라 콘텐츠 표시)

if menu == '폐차장 조회':
    show_scrapyard_finder()
elif menu == 'FAQ 검색 시스템':
    show_faq_system()
elif menu == '통계 시각화': # 통계 시각화 추가
    show_statistics()
elif menu == 'SQL 질의 실행':
    show_sql_executor()

