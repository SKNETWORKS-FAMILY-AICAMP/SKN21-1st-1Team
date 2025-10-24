"""
Author: 문지영
Date: 2025-10-22
Description: 폐차장 위치 검색 화면
"""
import streamlit.components.v1 as components 
import streamlit as st
import pandas as pd
import urllib.parse
import math, requests
import requests
import json
from pathlib import Path

# --------------------
# 설정(상수)
# --------------------
API_BASE_URL = "http://127.0.0.1:5000"
API_SCRAPYARD = f"{API_BASE_URL}/scrapyards"
API_FAQ_URL = f"{API_BASE_URL}/faqs"
API_SUBREGIONS_URL = f"{API_BASE_URL}/subregions" # 💡 [추가]
# 💡 [추가] 지역명 <-> 지역코드 변환 맵 (전역 변수로)
REGION_CODE_MAP = {"서울": "02", "경기": "01", "인천": "11"}

st.markdown("""

            
            
<style>
/* 파란색 검색 버튼 스타일 정의 */
.stButton>button {
    color: white;
    background-color: #1158e0; 
    border-radius: 5px;
    padding: 8px 16px;
    font-weight: bold;
    border: 1px solid #1158e0;
    /* 드롭다운 박스와 수직 위치를 맞추기 위해 마진 조정 */
    margin-top: 10px; 
}
            
/* st.info 위젯 내부 텍스트 중앙 정렬 및 패딩 조정 */
div[data-testid="stAlert"] div[role="alert"] {
    text-align: center; 
    padding-top: 15px;
    padding-bottom: 15px;
}

/* DataFrame 테이블 너비를 100%로 설정 */
.dataframe {
    width: 100%;
}
/* st.info 위젯 내부 텍스트 중앙 정렬 및 패딩 조정 */
div[data-testid="stAlert"] div[role="alert"] {
    text-align: center; 
    padding-top: 15px;
    padding-bottom: 15px;
}
/* 수동 테이블 구분선 스타일 */
.row-divider {
    margin: 0px 0;
    border: 0.5px solid #eee;
}
.header-divider {
    margin: 0px 0 10px 0;
    border: 1px solid #ddd;
}
/* 특정 클래스 내부 요소 중앙 정렬 /
.stVerticalBlock .st-emotion-cache-wfksaw.e196pkbe2 {
    display: flex;
    flex-direction: column;
    align-items: center;  / 가로 방향 중앙 정렬 /
    justify-content: center;  / 세로 방향 중앙 정렬 /
    text-align: center;  / 텍스트 중앙 정렬 */
}
</style>
""", unsafe_allow_html=True)
API_SCRAPYARD = "http://127.0.0.1:5000/scrapyards"
# --------------------
# API 호출 유틸
# --------------------
@st.cache_data
def check_api_base(url: str = API_BASE_URL, timeout: int = 3) -> bool:
    try:
        resp = requests.get(url, timeout=timeout)
        resp.raise_for_status()
        return True
    except requests.exceptions.RequestException:
        return False

@st.cache_data
def load_faq_from_api(url: str = API_FAQ_URL, timeout: int = 5):
    try:
        resp = requests.get(url, timeout=timeout)
        resp.raise_for_status()
        return resp.json()
    except requests.exceptions.RequestException:
        return []
@st.cache_data
def load_subregions_from_api(region_code: str, timeout: int = 5):
    """선택한 시/도에 해당하는 시/군/구 목록을 Flask API로부터 받아옵니다."""
    if not region_code:
        # '전체'를 선택했거나 맵에 없는 값이면 (region_code=None) 빈 리스트 반환
        return [] 
    
    try:
        params = {"region": region_code}
        resp = requests.get(API_SUBREGIONS_URL, params=params, timeout=timeout)
        resp.raise_for_status()
        # API는 ['강남구', '성동구', ...] 형태의 JSON 리스트를 반환
        return resp.json() 
    except requests.exceptions.RequestException as e:
        st.error(f"세부 지역 목록 로딩 실패: {e}")
        return []
def normalize_faq_list(data):
    if not isinstance(data, list):
        if isinstance(data, dict) and "data" in data and isinstance(data["data"], list):
            data = data["data"]
        else:
            return []
    normalized = []
    for item in data:
        if not isinstance(item, dict):
            continue
        q = item.get("Q") or item.get("QUESTION") or item.get("question")
        a = item.get("A") or item.get("ANSWER") or item.get("answer")
        src = item.get("출처") or item.get("source") or item.get("SOURCE") or ""
        if q and a:
            normalized.append({"Q": str(q).strip(), "A": str(a).strip(), "출처": str(src).strip()})
    return normalized

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
# SEOUL_DISTRICTS = ['강남구', '성북구', '성동구', '영등포구', '전체']
# GYEONGGI_CITIES = ['수원시', '성남시', '용인시', '화성시', '전체']
# INCHEON_DISTRICTS = ['연수구', '남동구', '부평구', '서구', '전체']

# REGION_DETAILS = {
#     '서울': SEOUL_DISTRICTS,
#     '경기': GYEONGGI_CITIES,
#     '인천': INCHEON_DISTRICTS,
#     '전체': ['전체']
# }

# --------------------
# 3. Mock Data (백엔드 대체 함수. 임의로 지정)
# --------------------
def get_scrapyard_list_with_address(selected_area, selected_district):
    """
    Flask API로 폐차장 데이터를 요청하여 DataFrame으로 반환
    """
    try:
        # Streamlit → Flask 쿼리 파라미터로 전달
        params = {}
        if selected_area not in ("", "전체"):
            # 💡 전역 맵(REGION_CODE_MAP) 사용
            params["region"] = REGION_CODE_MAP.get(selected_area) 
        if selected_district not in ("", "전체"):
            params["subregion"] = selected_district

        # Flask로 GET 요청
        response = requests.get(API_SCRAPYARD, params=params, timeout=5)
        response.raise_for_status()

        data = response.json()
        if not data:
            st.warning("조건에 맞는 폐차장 데이터가 없습니다.")
            return pd.DataFrame()

        # JSON → DataFrame
        df = pd.DataFrame(data)

        # 컬럼 이름 변경 (UI 표시에 맞게)
        df.rename(columns={
            "SY_NAME": "업체명",
            "ADDRESS": "주소",
            "CONTACT_NUMBER": "연락처",
            "REGION_CODE": "지역코드",
            "SUBREGION_NAME": "세부지역"
        }, inplace=True)

        return df

    except requests.exceptions.RequestException as e:
        st.error(f"🚨 Flask 서버 통신 오류: {e}")
        return pd.DataFrame()


# ----------------------------------------------------
# 🌟 콜백 함수: '검색' 버튼 클릭 시 실행
# ----------------------------------------------------
def perform_search_and_reset():
    """검색을 수행하고 페이지 및 지도 세션 상태를 초기화합니다."""
    # 드롭다운 위젯의 현재 값(세션 상태에 저장되어 있음)을 사용하여 검색
    selected_area = st.session_state.area_select # key="area_select"의 값
    selected_district = st.session_state.district_select # key="district_select"의 값
    
    # 1. 페이지 초기화
    st.session_state.current_page = 1
    st.session_state.map_info = {'address': None, 'url': None}
    
    # 2. DB 함수 호출 및 결과 저장
    result_df = get_scrapyard_list_with_address(selected_area, selected_district)
    st.session_state.last_search_df = result_df



# 1. 페이지 설정 (기존과 동일)
st.set_page_config(
    page_title="수도권 폐차장 조회 및 FAQ 시스템",
    page_icon="🚙",
    layout="wide",
    initial_sidebar_state="expanded"
)


# 2. 사이드바 메뉴 구현 (key 추가로 DuplicateElementId 오류 해결)
st.sidebar.title("⚙️ 시스템 메뉴")
menu = st.sidebar.radio(" ",
    ('폐차장 조회', 'FAQ 검색 시스템'),
    key='sidebar_menu' # <-- key 추가
)


# 세션 상태 초기화 (페이지네이션 및 지도)
if 'current_page' not in st.session_state:
    st.session_state.current_page = 1
if 'last_search_df' not in st.session_state:
    st.session_state.last_search_df = pd.DataFrame()
# 지도 임베드 정보를 위한 세션 상태 추가
if 'map_info' not in st.session_state:
    st.session_state.map_info = {'address': None, 'url': None}
    
# 검색 드롭다운 선택값을 위한 세션 상태 초기화 
if 'area_select' not in st.session_state:
    st.session_state.area_select = '전체'
if 'district_select' not in st.session_state:
    st.session_state.district_select = '전체'


# --------------------
# 5. 폐차장 조회 함수 
# --------------------
def show_scrapyard_finder():
    """ 폐차장 조회 페이지 (지도 임베드 기능 통합) """
    st.header ("🚙 수도권 폐차장 조회")
    
    st.write("원하는 지역과 세부 지역을 선택한 후 검색하세요.")

    col1, col2, col3 = st.columns([1, 1, 0.4])

    # 검색 조건을 세션 상태에 저장
    with col1:
        # 💡 [수정] 시/도 변경 시, 세부 지역을 '전체'로 리셋하는 on_change 콜백 추가
        st.selectbox(
            "지역별 검색 (시/도)",
            ['전체', '서울', '경기', '인천'],
            index = ['전체', '서울', '경기', '인천'].index(st.session_state.area_select),
            key="area_select",
            on_change=lambda: st.session_state.update(district_select='전체')
        )
    
    # 💡 [수정] API를 통해 세부 지역 목록 동적 로드
    selected_region_name = st.session_state.area_select
    selected_region_code = REGION_CODE_MAP.get(selected_region_name) # e.g., '02' or None
    
    # API 호출 (캐시되어 있으므로 빠름)
    detail_options_from_db = load_subregions_from_api(selected_region_code) 
    
    # DB에서 가져온 목록 앞에 항상 '전체' 옵션을 추가
    detail_options = ['전체'] + detail_options_from_db

    with col2:
        # 💡 [삭제] detail_options = REGION_DETAILS.get(st.session_state.area_select, ['전체'])

        # 💡 [추가] 시/도를 변경했을 때, 이전에 선택한 세부 지역이 새 목록에 없으면 '전체'로 강제 리셋
        current_district = st.session_state.district_select
        if current_district not in detail_options:
            current_district = '전체'
            st.session_state.district_select = '전체' # 세션 상태도 '전체'로 업데이트
        
        st.selectbox(
            f"'{st.session_state.area_select}'의 세부 지역 검색 (구/시)",
            detail_options, # 💡 API로 받아온 동적 목록 사용
            index=detail_options.index(current_district),
            key="district_select"
        )
    # 검색 버튼 (콜백 함수 사용)
    with col3:
        st.markdown('<div class="blue-button">', unsafe_allow_html=True)
        # '검색' 버튼 클릭 시 perform_search_and_reset 함수가 실행되고 st.rerun() 됨
        st.button("검색", on_click=perform_search_and_reset, key="search_button_widget", use_container_width=True) 
        st.markdown('</div>', unsafe_allow_html=True)    
                        
        

# -----------------------------------------------------------------
# 페이징 및 결과 출력 영역
# -----------------------------------------------------------------
    
    if not st.session_state.last_search_df.empty:
        
        result_df = st.session_state.last_search_df
        total_rows = len(result_df)
        page_size = 5
        total_pages = math.ceil(total_rows / page_size)
        current_page = st.session_state.current_page

        st.subheader(f"🔍 조회 결과 (**{total_rows}**건)")

        # 현재 페이지에 해당하는 데이터 슬라이싱
        start_row = (current_page - 1) * page_size
        end_row = start_row + page_size
        paginated_df = result_df.iloc[start_row:end_row].copy()


        # 결과 테이블 헤더 수동 생성
        # (이전 요청에 따른 버튼 너비 해결을 위해 4번째 컬럼 비율 조정된 것 유지)
        header_cols = st.columns([2.5, 2.5, 2.0, 2.0]) 
        header_cols[0].markdown('**업체명**')
        header_cols[1].markdown('**주소**')
        header_cols[2].markdown('**연락처**')
        header_cols[3].markdown('**지도**')

        st.markdown('<hr class="header-divider"/>', unsafe_allow_html=True) # 헤더와 내용 구분선

        
        # 결과 테이블 내용 수동 생성 (버튼 통합)
        for index, row in paginated_df.iterrows():
            # (이전 요청에 따른 버튼 너비 해결을 위해 4번째 컬럼 비율 조정된 것 유지)
            row_cols = st.columns([2.5, 3.5, 1.5, 2.0]) # 너비 비율은 헤더와 동일하게 유지
            
            # 업체명 (링크 대신 텍스트 출력)
            row_cols[0].markdown(f"**{row['업체명']}**", unsafe_allow_html=True)
            
            # 주소
            row_cols[1].markdown(row['주소'])
            
            # 연락처
            row_cols[2].markdown(row['연락처'])

            # '지도 보기' 버튼 (버튼 클릭 시 지도 임베드)
            with row_cols[3]:
                if st.button("🗺️ 지도 보기", key=f"mapbtn{row['SY_ID']}", use_container_width=True):
                    st.session_state.map_info['address'] = row['주소']
                    st.session_state.map_info['url'] = get_kakao_map_iframe_url(row['주소'])
                    st.rerun()
            
            # 각 행의 중간 구분선 추가
            st.markdown('<hr class="row-divider"/>', unsafe_allow_html=True)
        
        # 3. 페이지 이동 버튼
        st.markdown("---")
        col_prev, col_page_info, col_next = st.columns([1, 2, 1])
        
        with col_prev:
            if current_page > 1:
                # 이전 페이지 버튼 클릭 시 세션 상태 current_page만 변경
                if st.button("⬅️ 이전 페이지"):
                    st.session_state.current_page -= 1
                    st.rerun()

        with col_page_info:
            st.markdown(f"<div style='text-align:center;'>페이지 {current_page} / {total_pages}</div>", unsafe_allow_html=True)
            
        with col_next:
            if current_page < total_pages:
                # 다음 페이지 버튼 클릭 시 세션 상태 current_page만 변경
                if st.button("다음 페이지 ➡️"):
                    st.session_state.current_page += 1
                    st.rerun()

    else:
        # 검색 결과가 없을 때 (초기 상태 포함)
        st.info("검색 조건을 선택하고 '검색' 버튼을 눌러주세요.")


    # 🌟 5-3. 지도 임베드 영역 (함수 마지막에 위치) ------------------
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
# 6. FAQ 시스템 함수 (검색 기능 제거, expander로 목록 표시)
# ----------------------------------------------------
def show_faq_system():
    st.header("❓ 폐차 관련 자주 묻는 질문 (FAQ)")
    st.write("자주 묻는 질문 목록입니다. 질문을 클릭하시면 답변을 확인할 수 있습니다.")

    # 서버 연결 여부 확인
    if not check_api_base():
        st.error(f"서버({API_BASE_URL})에 연결할 수 없습니다. 서버가 실행 중인지 확인하세요.")
        return

    raw = load_faq_from_api()
    if not raw:
        st.info("FAQ 데이터를 불러오지 못했습니다. (API 응답 없음)")
        return

    faq_list = normalize_faq_list(raw)
    if not faq_list:
        st.warning("API 응답을 받았으나 유효한 FAQ 데이터가 없습니다.")
        return

    df = pd.DataFrame(faq_list)
    for i, row in df.iterrows():
        q = row.get("Q", "")
        a = row.get("A", "")
        src = row.get("출처", "")
        with st.expander(f"Q{i+1}. {q}"):
            st.markdown(a)
            if src:
                st.caption(f"출처: {src}")

# --------------------
# 메인 라우팅
# --------------------
if menu == '폐차장 조회':
    show_scrapyard_finder()
elif menu == 'FAQ 검색 시스템':
    show_faq_system()