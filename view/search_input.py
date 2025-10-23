"""
Author: 문지영
Date: 2025-10-22
Description: 폐차장 위치 검색 화면
"""
import streamlit as st
import pandas as pd
import urllib.parse
import math
import streamlit.components.v1 as components # st.components.v1.html 사용을 위해 추가


st.markdown("""
<style>
/* 빨간색 검색 버튼 스타일 정의 */
.stButton>button {
    color: white;
    background-color: #FF4B4B; 
    border-radius: 5px;
    padding: 8px 16px;
    font-weight: bold;
    border: 1px solid #FF4B4B;
    /* 드롭다운 박스와 수직 위치를 맞추기 위해 마진 조정 */
    margin-top: 25px; 
}
/* st.info 위젯 내부 텍스트 중앙 정렬 및 패딩 조정 */
div[data-testid="stAlert"] div[role="alert"] {
    text-align: center; 
    padding-top: 15px;
    padding-bottom: 15px;
}

/* 🌟 추가: 수동으로 만든 테이블의 구분선 스타일 */
.row-divider {
    margin: 0px 0;
    border: 0.5px solid #eee;
}
.header-divider {
    margin: 0px 0 10px 0;
    border: 1px solid #ddd;
}
</style>
""", unsafe_allow_html=True)


# --------------------
# 1. 카카오맵 URL 생성 함수 (상단에 정의)
# --------------------
def create_kakaomap_url(address):
    """주소를 카카오맵 검색 URL로 인코딩하여 새 창으로 여는 URL을 반환합니다."""
    base_url = "https://map.kakao.com/"
    encoded_address = urllib.parse.quote(address)
    return f"{base_url}?q={encoded_address}"

def get_kakao_map_iframe_url(address):
    """주소를 카카오맵 iframe 임베딩용 URL로 인코딩하여 반환합니다. (검색창 숨김)"""
    # 카카오맵 개발자 API를 사용하지 않고 iframe 검색 기능을 활용합니다.
    encoded_address = urllib.parse.quote(address)
    # 맵 주소 + 검색어를 iframe에 바로 넣으면 됩니다.
    return f"https://map.kakao.com/?q={encoded_address}&map_type=TYPE_MAP&src=internal"

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
        # 🌟 ID 추가: 버튼 고유 키 생성에 사용
        'ID': range(1, 82), 
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


# 1. 페이지 설정 (기존과 동일)
st.set_page_config(
    page_title="수도권 폐차장 조회 및 FAQ 시스템",
    page_icon="🚙",
    layout="wide",
    initial_sidebar_state="expanded"
)


# 2. 사이드바 메뉴 구현 (기존과 동일)
st.sidebar.title("⚙️ 시스템 메뉴")
menu = st.sidebar.radio(" ",
    ('폐차장 조회', 'FAQ 검색 시스템', '통계 시각화', 'SQL 질의 진행')
)


# 🌟 세션 상태 초기화 (페이지네이션 및 지도)
if 'current_page' not in st.session_state:
    st.session_state.current_page = 1
if 'last_search_df' not in st.session_state:
    st.session_state.last_search_df = pd.DataFrame()
# 🌟 지도 임베드 정보를 위한 세션 상태 추가
if 'map_info' not in st.session_state:
    st.session_state.map_info = {'address': None, 'url': None}


# --------------------
# 5. 폐차장 조회 함수 (페이징 기능 추가)
# --------------------
def show_scrapyard_finder():
    """ 폐차장 조회 페이지 (지도 임베드 기능 통합) """
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
        if st.button("검색", use_container_width=True, key="search_button"):
            # 검색 시 항상 첫 페이지로 초기화 및 지도 정보 삭제
            st.session_state.current_page = 1
            st.session_state.map_info = {'address': None, 'url': None}
        
            # 🚨 DB 함수 호출 및 결과 저장
            result_df = get_scrapyard_list_with_address(selected_area, selected_district)
            st.session_state.last_search_df = result_df
        
            st.info(f"선택 지역: **{selected_area}** / **{selected_district}** 에 대한 폐차장 정보를 조회합니다.")


# -----------------------------------------------------------------
# 🌟 페이징 및 결과 출력 영역
# -----------------------------------------------------------------
    
    if not st.session_state.last_search_df.empty:
        
        result_df = st.session_state.last_search_df
        total_rows = len(result_df)
        page_size = 5
        total_pages = math.ceil(total_rows / page_size)
        current_page = st.session_state.current_page
        
        st.success(f"검색 조건에 맞는 폐차장 **{total_rows}** 건을 찾았습니다. (총 {total_pages} 페이지)")

        # 현재 페이지에 해당하는 데이터 슬라이싱
        start_row = (current_page - 1) * page_size
        end_row = start_row + page_size
        paginated_df = result_df.iloc[start_row:end_row].copy()


        # 🌟 결과 테이블 헤더 수동 생성
        header_cols = st.columns([2.5, 3.5, 1.5, 1.5])
        header_cols[0].markdown('**업체명**')
        header_cols[1].markdown('**주소**')
        header_cols[2].markdown('**연락처**')
        header_cols[3].markdown('**지도**')
        st.markdown('<hr class="header-divider"/>', unsafe_allow_html=True) # 헤더와 내용 구분선

        
        # 🌟 결과 테이블 내용 수동 생성 (버튼 통합)
        for index, row in paginated_df.iterrows():
            row_cols = st.columns([2.5, 3.5, 1.5, 1.5]) # 너비 비율은 헤더와 동일하게 유지
            
            # 업체명 (링크 대신 텍스트 출력)
            row_cols[0].markdown(f"**{row['업체명']}**", unsafe_allow_html=True)
            
            # 주소
            row_cols[1].markdown(row['주소'])
            
            # 연락처
            row_cols[2].markdown(row['연락처'])

            # 🌟 '지도 보기' 버튼 (버튼 클릭 시 지도 임베드)
            with row_cols[3]:
                # 업체명 대신 '지도 보기' 버튼 클릭으로 임베드 기능 구현
                if st.button("🗺️ 지도 보기", key=f"mapbtn{row['ID']}", use_container_width=True):
                    st.session_state.map_info['address'] = row['주소']
                    st.session_state.map_info['url'] = get_kakao_map_iframe_url(row['주소'])
                    st.rerun()
            
            # 각 행의 중간 구분선 추가
            st.markdown('<hr class="row-divider"/>', unsafe_allow_html=True)
        
        # 3. 페이지 이동 버튼 (기존과 동일)
        st.markdown("---")
        col_prev, col_page_info, col_next = st.columns([1, 2, 1])
        
        with col_prev:
            if current_page > 1:
                if st.button("⬅️ 이전 페이지"):
                    st.session_state.current_page -= 1
                    st.rerun()

        with col_page_info:
            st.markdown(f"<div style='text-align:center;'>페이지 {current_page} / {total_pages}</div>", unsafe_allow_html=True)
            
        with col_next:
            if current_page < total_pages:
                if st.button("다음 페이지 ➡️"):
                    st.session_state.current_page += 1
                    st.rerun()

    else:
        # ... (결과 없음 로직)
        pass

    # ------------------ 🌟 5-3. 지도 임베드 영역 (함수 마지막에 위치) ------------------
    if st.session_state.map_info['address']:
        import streamlit.components.v1 as components # 함수 내에서 다시 import
        st.markdown("---")
        st.subheader(f"🗺️ 위치 확인: {st.session_state.map_info['address']}")

        map_url = st.session_state.map_info['url']

        # 카카오 지도 iframe 임베드
        components.html(
            f"""
            <iframe 
                width="100%" 
                height="500" 
                frameborder="0" 
                scrolling="no" 
                marginwidth="0" 
                marginheight="0" 
                src="{map_url}"
            >
            </iframe>
            """,
            height=520, # iframe 높이
        )
# ----------------------------------------------------


# ----------------------------------------------------
# FAQ 시스템 함수 (기존과 동일)
# ----------------------------------------------------
def show_faq_system():
    """[2] FAQ 검색 시스템 페이지"""
    st.header("❓ 폐차 관련 자주 묻는 질문 (FAQ)")
    st.write("궁금한 키워드를 입력하시면 관련된 질문과 답변을 찾아드립니다.")
    
    # 사용자 입력: 검색 키워드 위젯
    keyword = st.text_input("검색 키워드 입력", max_chars=50, key="faq_keyword")
    
    if st.button("FAQ 검색", key="faq_search_btn"):
        if keyword:
            faq_list = search_faq(keyword)
            
            if faq_list:
                st.info(f"'{keyword}'와(과) 관련된 FAQ **{len(faq_list)}** 건이 검색되었습니다.")
                
                for i, item in enumerate(faq_list):
                    with st.expander(f"**Q{i+1}.** {item['Q']}"):
                        st.markdown(f"**A.** {item['A']}")
                        st.caption(f"**출처:** {item['출처']}")
            else:
                st.warning(f"'{keyword}'와(과) 관련된 질문을 찾을 수 없습니다.")
        else:
            st.error("검색 키워드를 입력해주세요.")


# 4. 메인 라우팅 (기존과 동일)
if menu == '폐차장 조회':
    show_scrapyard_finder()
elif menu == 'FAQ 검색 시스템':
    show_faq_system()