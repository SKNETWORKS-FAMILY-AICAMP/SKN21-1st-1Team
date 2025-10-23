"""
Author: 문지영
Date: 2025-10-22
Description: 폐차장 위치 검색 화면
"""

import streamlit as st
import pandas as pd
import urllib.parse
import math


st.markdown("""
<style>
/* 빨간색 검색 버튼 스타일 정의 */
.stButton>button {
    color: white;
    background-color: #FF4B4B; /* Streamlit 기본 빨간색 */
    border-radius: 5px;
    padding: 8px 16px;
    font-weight: bold;
    border: 1px solid #FF4B4B;
    /* 🌟 핵심 수정: 드롭다운 박스와 수직 위치를 맞추기 위해 마진 조정 */
    margin-top: 25px; /* 30px에서 25px로 조정하여 높이를 맞춥니다. */
}
/* DataFrame 테이블 너비를 100%로 설정 (좌우 간격 맞추기) */
.dataframe {
    width: 100%;
}
</style>
""", unsafe_allow_html=True)



# --------------------
# 1. 카카오맵 URL 생성 함수 (상단에 정의)
# --------------------
def create_kakaomap_url(address):
    """주소를 카카오맵 검색 URL로 인코딩하여 반환합니다."""
    base_url = "https://map.kakao.com/"
    encoded_address = urllib.parse.quote(address)
    return f"{base_url}?q={encoded_address}"

# --------------------
# 지역별 세부 구/시 데이터 정의 (전역 변수 위치. 임의로 지정.)
# --------------------
SEOUL_DISTRICTS = ['강남구', '성북구', '성동구', '영등포구', '전체']
GYEONGGI_CITIES = ['수원시', '성남시', '용인시', '화성시', '전체']
INCHEON_DISTRICTS = ['연수구', '남동구', '부평구', '서구', '전체']

REGION_DETAILS = {
    '서울': SEOUL_DISTRICTS,
    '경기': GYEONGGI_CITIES,
    '인천': INCHEON_DISTRICTS,
    '전체': ['전체']
}

# --------------------
# 3. Mock Data (백엔드 대체 함수. 임의로 지정)
# --------------------
def get_scrapyard_list_with_address(selected_area, selected_district):
    data = {
        '업체명': [f'{area} {dist} 폐차장 {i}' for area in ['서울', '경기', '인천'] for dist in ['강남구', '수원시', '부평구'] for i in range(1, 10)],
        '지역': [area for area in ['서울', '경기', '인천'] for dist in ['강남구', '수원시', '부평구'] for i in range(1, 10)],
        '세부지역': [dist for area in ['서울', '경기', '인천'] for dist in ['강남구', '수원시', '부평구'] for i in range(1, 10)],
        '주소': [f'{area} {dist} 주소 {i}' for area in ['서울', '경기', '인천'] for dist in ['강남구', '수원시', '부평구'] for i in range(1, 10)],
        '연락처': [f'02-{i:03d}-xxxx' for i in range(1, 82)]
    }
    df = pd.DataFrame(data)
    
    # Mock 필터링 로직
    if selected_area != '전체':
        df = df[df['지역'] == selected_area]
        if selected_district != '전체':
             df = df[df['세부지역'] == selected_district]
             
    return df.reset_index(drop=True)


# --------------------
# 4. Mock Data for FAQ 검색 (search_faq 함수 정의. 임의로 지정)
# --------------------
def search_faq(keyword):
    # Mock Data for FAQ 검색
    faq_data = [
        {'Q': '폐차 절차는 어떻게 되나요?', 'A': '차량 소유자는 신분증 사본과 자동차 등록증을 준비하여 폐차장에 인계하면 됩니다.', '출처': 'KADRA'},
        {'Q': '자동차를 폐차하면 환급받을 수 있는 것이 있나요?', 'A': '자동차세 선납분과 보험료 잔여액을 환급받을 수 있습니다.', '출처': 'KADRA'},
        {'Q': '압류나 저당이 잡혀 있어도 폐차가 가능한가요?', 'A': '차령초과말소 제도(선폐차)를 통해 가능합니다.', '출처': 'KADRA'},
        {'Q': '폐차는 어디서 해야 하나요?', 'A': '관허 폐차장을 이용해야 합니다.', '출처': 'KADRA'},
    ]
    
    # 키워드와 관련된 FAQ만 필터링합니다.
    if not keyword:
        return []
        
    filtered_faq = [item for item in faq_data if keyword.lower() in item['Q'].lower() or keyword.lower() in item['A'].lower()]
    return filtered_faq
# --------------------





# 1. 페이지 설정
st.set_page_config(
    page_title="수도권 폐차장 조회 및 FAQ 시스템",
    page_icon="🚙",
    layout="wide",
    initial_sidebar_state="expanded"
)


# 2. 사이드바 메뉴 구현
st.sidebar.title("⚙️ 시스템 메뉴")
menu = st.sidebar.radio(" ",
    #('🚙 폐차장 조회', '❓ FAQ 검색 시스템', '📊 통계 시각화', '🙋🏻‍♀️ SQL 질의 진행')
    ('폐차장 조회', 'FAQ 검색 시스템', '통계 시각화', 'SQL 질의 진행')
)


# 세션 상태 초기화 (페이지네이션)
if 'current_page' not in st.session_state:
    st.session_state.current_page = 1
if 'last_search_df' not in st.session_state:
    st.session_state.last_search_df = pd.DataFrame()


# --------------------
# 5. 폐차장 조회 함수 (페이징 기능 추가)
# --------------------
def show_scrapyard_finder():
    """ 폐차장 조회 페이지 (카카오맵 연결 포함) """
    st.header ("📍수도권 폐차장 조회")
    st.write("원하는 지역과 세부 지역을 선택한 후 검색하세요.")

    col1, col2, col3 = st.columns([1, 1, 0.5])

    with col1:
        selected_area = st.selectbox(
            "지역별 검색 (시/도)",
            ['전체', '서울', '경기', '인천'],
            index = 0,
            key="area_select"
        )
    
    with col2:
        detail_options = REGION_DETAILS.get(selected_area, ['전체'])
        selected_district = st.selectbox(
            f"'{selected_area}'의 세부 지역 검색 (구/시)",
            detail_options,
            index=detail_options.index('전체') if '전체' in detail_options else 0,
            key="district_select"
        )

    # 검색 버튼
    with col3:
        # st.button 앞에 아무 위젯도 넣지 않고 CSS의 margin-top으로 높이를 맞춥니다.
        if st.button("검색", use_container_width=True, key="search_button"):

            # 검색 시 항상 첫 페이지로 초기화
            st.session_state.current_page = 1
        
            # 🚨 DB 함수 호출 및 결과 저장
            result_df = get_scrapyard_list_with_address(selected_area, selected_district)
            st.session_state.last_search_df = result_df # 세션 상태에 전체 검색 결과 저장
        
            st.info(f"선택 지역: **{selected_area}** / **{selected_district}** 에 대한 폐차장 정보를 조회합니다.")


# -----------------------------------------------------------------
# 🌟 페이징 및 결과 출력 영역
# -----------------------------------------------------------------
    
    if not st.session_state.last_search_df.empty:
        
        result_df = st.session_state.last_search_df # 저장된 전체 결과 사용
        total_rows = len(result_df)
        page_size = 5 # 한 페이지당 보여줄 개수
        total_pages = math.ceil(total_rows / page_size)
        current_page = st.session_state.current_page
        
        st.success(f"검색 조건에 맞는 폐차장 **{total_rows}** 건을 찾았습니다. (총 {total_pages} 페이지)")

        # 현재 페이지에 해당하는 데이터 슬라이싱
        start_row = (current_page - 1) * page_size
        end_row = start_row + page_size
        paginated_df = result_df.iloc[start_row:end_row].copy()


        # 1. 카카오맵 링크 생성 및 버튼 추가
        paginated_df['지도 보기'] = paginated_df['주소'].apply(
            lambda addr: f'<a href="{create_kakaomap_url(addr)}" target="_blank">지도 보기</a>'
        )
        
        # 2. 결과 표 출력 (st.dataframe 대신 HTML 마크다운 사용)
        st.markdown(
            paginated_df[['업체명', '주소', '연락처', '지도 보기']].to_html(escape=False, index=False), 
            unsafe_allow_html=True
        )
        
        # 3. 페이지 이동 버튼 (페이징 버튼)
        st.markdown("---")
        col_prev, col_page_info, col_next = st.columns([1, 2, 1])
        
        with col_prev:
            if current_page > 1:
                if st.button("⬅️ 이전 페이지"):
                    st.session_state.current_page -= 1
                    st.rerun() # 페이지 이동 후 재실행

        with col_page_info:
            st.markdown(f"<div style='text-align:center;'>페이지 **{current_page}** / **{total_pages}**</div>", unsafe_allow_html=True)
            
        with col_next:
            if current_page < total_pages:
                if st.button("다음 페이지 ➡️"):
                    st.session_state.current_page += 1
                    st.rerun() # 페이지 이동 후 재실행

    else:
        # 최초 로딩 시 또는 검색 결과 없을 때
        if st.session_state.last_search_df.empty and 'current_page' in st.session_state and st.session_state.current_page > 1:
            st.warning("검색 결과가 없습니다.")
        elif 'current_page' in st.session_state and st.session_state.current_page == 1:
            # 첫 페이지 로딩 시 메시지 없음
            pass
# ----------------------------------------------------



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



