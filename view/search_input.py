"""
Author: 문지영
Date: 2025-10-22
Description: 폐차장 위치 검색 화면
"""

# Data 화면 출력을 위한 streamlit 코드 작성.
# TODO 지영님 Streamlit 활용하여 화면 작성 필요.

import streamlit as st
import pandas as pd


# 지역별로 했을 때 갯수 
# 페이지 처리하기. 
# 만약 조회했는데 50개 나오면 한 화면이 아니라 임의로 5개 정도 설정하고 
# 테이블 박스로 줄텐데 동적으로 처리하기. 길면 맞춰지게끔. 

# 업체명 누르면 지도에 찍히게.



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




def show_faq_system():
    """[2] FAQ 검색 시스템 페이지"""
    st.header("❓ 폐차 관련 자주 묻는 질문 (FAQ)")
    st.write("궁금한 키워드를 입력하시면 관련된 질문과 답변을 찾아드립니다.")
    
    # 사용자 입력: 검색 키워드 위젯
    keyword = st.text_input("검색 키워드 입력", max_chars=50, key="faq_keyword")
    
    if st.button("FAQ 검색"):
        if keyword:
            # 🚨 DB 함수 호출 (현재는 Mock 함수 사용)
            faq_list = search_faq(keyword)
            
            if faq_list:
                st.info(f"'{keyword}'와(과) 관련된 FAQ **{len(faq_list)}** 건이 검색되었습니다.")
                
                # 검색 결과를 확장 가능한 형태로 출력
                for i, item in enumerate(faq_list):
                    # st.expander를 사용하여 답변을 숨겨 사용자 경험 향상
                    with st.expander(f"**Q{i+1}.** {item['Q']}"):
                        st.markdown(f"**A.** {item['A']}")
                        st.caption(f"**출처:** {item['출처']}") # 출처 표기
            else:
                st.warning(f"'{keyword}'와(과) 관련된 질문을 찾을 수 없습니다.")
        else:
            st.error("검색 키워드를 입력해주세요.")



# 4. 메인 라우팅 
if menu == '폐차장 조회':
    show_scrapyard_finder()
elif menu == 'FAQ 검색 시스템':
    show_faq_system()



