"""
Author: 문지영
Date: 2025-10-22
Description: 폐차장 위치 검색 화면
"""

import streamlit.components.v1 as components 
import streamlit as st
import pandas as pd
import urllib.parse
import math


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
    encoded_address = urllib.parse.quote(address)
    return f"https://map.kakao.com/?q={encoded_address}&map_type=TYPE_MAP&src=internal"

# --------------------
# 2. 실제 JSON 데이터 정의 및 DataFrame 변환 (70개 데이터 생성)
# --------------------
# 제공해주신 6개 JSON 데이터의 패턴을 사용하여 70개의 데이터 생성 가정
BASE_DATA_PATTERN = [
    {"SUBREGION_NAME": "금천구", "CEO_NAME": "박순용", "ADDRESS": "서울 금천구 두산로 23 (독산동)"}, 
    {"SUBREGION_NAME": "성동구", "CEO_NAME": "황계식", "ADDRESS": "서울특별시 성동구 성수이로22길 54"}, 
    {"SUBREGION_NAME": "성동구", "CEO_NAME": "윤석규", "ADDRESS": "서울특별시 성동구 상원길 73-1"}, 
    {"SUBREGION_NAME": "도봉구", "CEO_NAME": "강창한", "ADDRESS": "서울 도봉구 덕릉로 63길,109(창2동)"}, 
    {"SUBREGION_NAME": "동대문구", "CEO_NAME": "이춘호", "ADDRESS": "서울특별시 동대문구 장안벚꽃로 9 (장안동)"}, 
    {"SUBREGION_NAME": "도봉구", "CEO_NAME": "윤길용", "ADDRESS": "서울특별시 도봉구 도봉로 632"},
]

# 70개 이상 데이터 생성을 위한 확장 로직 (실제 데이터가 들어올 위치)
SCRAPYARD_DATA_JSON_EXPANDED = []
NUM_RECORDS = 70 # 70개의 데이터 생성 가정 (100개 미만)

for i in range(NUM_RECORDS):
    base_index = i % len(BASE_DATA_PATTERN)
    base = BASE_DATA_PATTERN[base_index]
    
    sy_id = i + 1
    contact_num = f"02-{sy_id:03d}-{i*10:04d}" 
    
    new_record = {
        "SY_ID": sy_id,
        "SY_NAME": f"관허폐차장서울영업소{sy_id}", 
        "CEO_NAME": base["CEO_NAME"],
        "CONTACT_NUMBER": contact_num,
        "ADDRESS": base["ADDRESS"].replace(base["SUBREGION_NAME"], base["SUBREGION_NAME"] + f"_{sy_id % 3}"), 
        "REGION_CODE": "02",
        "SUBREGION_NAME": base["SUBREGION_NAME"],
    }
    SCRAPYARD_DATA_JSON_EXPANDED.append(new_record)

# DataFrame 생성 및 컬럼 이름 변경
SCRAPYARD_DF_RAW = pd.DataFrame(SCRAPYARD_DATA_JSON_EXPANDED)

if not SCRAPYARD_DF_RAW.empty:
    # 예시 데이터는 모두 서울(REGION_CODE '02')이므로 '지역' 컬럼을 '서울'로 통일
    SCRAPYARD_DF_RAW['지역'] = '서울' 
    SCRAPYARD_DF_RAW.rename(columns={'SUBREGION_NAME': '세부지역', 'ADDRESS': '주소', 'SY_NAME': '업체명', 'CONTACT_NUMBER': '연락처', 'SY_ID': 'ID'}, inplace=True)
    SCRAPYARD_DF_RAW = SCRAPYARD_DF_RAW[['ID', '업체명', '지역', '세부지역', '주소', '연락처']]
else:
    SCRAPYARD_DF_RAW = pd.DataFrame(columns=['ID', '업체명', '지역', '세부지역', '주소', '연락처'])


# --------------------
# 지역별 세부 구/시 데이터 정의 (동적으로 생성)
# --------------------

# 데이터프레임에서 존재하는 지역 및 세부지역 목록을 추출
ALL_REGIONS = SCRAPYARD_DF_RAW['지역'].unique().tolist()

# '서울', '경기', '인천' 등 주요 지역을 정의
# 실제 데이터에 맞게 동적으로 '세부지역' 목록을 만듭니다.

REGION_DETAILS = {}
# 주요 지역(시/도)에 '전체'가 포함되지 않도록 먼저 유니크 목록을 가져옵니다.
PRIMARY_REGIONS = ['서울', '경기', '인천'] # 이 목록은 하드코딩

for region in PRIMARY_REGIONS:
    if region in ALL_REGIONS:
        # 해당 지역에 해당하는 세부 지역 (구/시) 목록을 DataFrame에서 추출
        sub_regions = SCRAPYARD_DF_RAW[SCRAPYARD_DF_RAW['지역'] == region]['세부지역'].unique().tolist()
        # 목록을 정렬하고 '전체' 옵션을 추가합니다.
        sub_regions.sort()
        REGION_DETAILS[region] = ['전체'] + sub_regions
    else:
        # 해당 지역에 데이터가 없으면 '전체'만 포함
        REGION_DETAILS[region] = ['전체']

# '전체' 지역 옵션 추가
REGION_DETAILS['전체'] = ['전체']


# --------------------
# 3. 데이터 필터링 함수 (실제 데이터프레임 사용)
# --------------------
def get_scrapyard_list_with_address(selected_area, selected_district):
    df = SCRAPYARD_DF_RAW.copy()
    
    # 지역 필터링
    if selected_area != '전체':
        df = df[df['지역'] == selected_area]
        
    # 세부 지역 필터링
    if selected_district != '전체':
         df = df[df['세부지역'] == selected_district]
             
    return df.reset_index(drop=True)


# ----------------------------------------------------
# 콜백 함수: '검색' 버튼 클릭 시 실행 
# ----------------------------------------------------
def perform_search_and_reset():
    """검색을 수행하고 페이지 및 지도 세션 상태를 초기화합니다."""
    selected_area = st.session_state.area_select 
    selected_district = st.session_state.district_select 
    
    st.session_state.current_page = 1
    st.session_state.map_info = {'address': None, 'url': None}
    
    result_df = get_scrapyard_list_with_address(selected_area, selected_district)
    st.session_state.last_search_df = result_df


# 1. 페이지 설정 
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
    key='sidebar_menu'
)


# 세션 상태 초기화 (페이지네이션 및 지도)
if 'current_page' not in st.session_state:
    st.session_state.current_page = 1
if 'last_search_df' not in st.session_state:
    # 초기 로드 시 전체 데이터를 검색하여 DF에 저장합니다.
    st.session_state.last_search_df = get_scrapyard_list_with_address('전체', '전체')
if 'map_info' not in st.session_state:
    st.session_state.map_info = {'address': None, 'url': None}
    
# 검색 드롭다운 선택값을 위한 세션 상태 초기화 
if 'area_select' not in st.session_state:
    st.session_state.area_select = '전체'
if 'district_select' not in st.session_state:
    st.session_state.district_select = '전체'


# --------------------
# 5. 폐차장 조회 함수 (세부지역 동적 목록 반영)
# --------------------
def show_scrapyard_finder():
    """ 폐차장 조회 페이지 (지도 임베드 기능 통합) """
    st.header ("🚙 수도권 폐차장 조회")
    
    st.write("원하는 지역과 세부 지역을 선택한 후 검색하세요.")

    col1, col2, col3 = st.columns([1, 1, 0.4])

    # 검색 조건을 세션 상태에 저장 (key를 사용해 st.session_state에 자동 저장됨)
    with col1:
        # 지역 드롭다운 옵션은 ['전체', '서울', '경기', '인천'] 고정 (데이터 유무와 관계없이)
        area_options = ['전체', '서울', '경기', '인천']
        st.selectbox(
            "지역별 검색 (시/도)",
            area_options,
            index = area_options.index(st.session_state.area_select),
            key="area_select"
        )
    
    with col2:
        # **선택된 지역에 따라 REGION_DETAILS에서 동적으로 옵션을 가져옴**
        detail_options = REGION_DETAILS.get(st.session_state.area_select, ['전체'])
        
        # 이전 선택값(st.session_state.district_select)이 현재 옵션 목록에 없으면 '전체'로 초기화
        if st.session_state.district_select not in detail_options:
            initial_district_index = 0 # '전체'
            st.session_state.district_select = '전체'
        else:
            initial_district_index = detail_options.index(st.session_state.district_select)
            
        st.selectbox(
            f"'{st.session_state.area_select}'의 세부 지역 검색 (구/시)",
            detail_options,
            index=initial_district_index,
            key="district_select"
        )

    # 검색 버튼 (콜백 함수 사용)
    with col3:
        st.markdown('<div class="blue-button">', unsafe_allow_html=True)
        st.button("검색", on_click=perform_search_and_reset, key="search_button_widget", use_container_width=True) 
        st.markdown('</div>', unsafe_allow_html=True)    
                        
        

# -----------------------------------------------------------------
# 페이징 및 결과 출력 영역 (기존과 동일)
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
        header_cols = st.columns([2.5, 2.5, 2.0, 2.0]) 
        header_cols[0].markdown('**업체명**')
        header_cols[1].markdown('**주소**')
        header_cols[2].markdown('**연락처**')
        header_cols[3].markdown('**지도**')

        st.markdown('<hr class="header-divider"/>', unsafe_allow_html=True) # 헤더와 내용 구분선

        
        # 결과 테이블 내용 수동 생성 (버튼 통합)
        for index, row in paginated_df.iterrows():
            row_cols = st.columns([2.5, 3.5, 1.5, 2.0]) # 너비 비율은 헤더와 동일하게 유지
            
            # 업체명 (링크 대신 텍스트 출력)
            row_cols[0].markdown(f"**{row['업체명']}**", unsafe_allow_html=True)
            
            # 주소
            row_cols[1].markdown(row['주소'])
            
            # 연락처
            row_cols[2].markdown(row['연락처'])

            # '지도 보기' 버튼 (버튼 클릭 시 지도 임베드)
            with row_cols[3]:
                if st.button("🗺️ 지도 보기", key=f"mapbtn{row['ID']}", use_container_width=True):
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
        # 검색 결과가 없을 때
        st.info("선택한 조건과 일치하는 폐차장 정보가 없습니다.")


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
# 6. FAQ 시스템 함수 (기존과 동일)
# ----------------------------------------------------
def show_faq_system():
    """[2] FAQ 검색 시스템 페이지: 검색 대신 FAQ 목록을 바로 표시합니다."""
    st.header("❓ 폐차 관련 자주 묻는 질문 (FAQ)")
    st.write("자주 묻는 질문 목록입니다. 질문을 클릭하시면 답변을 확인할 수 있습니다.")
    
    # FAQ 데이터 정의 (검색 기능 제거 후 사용)
    faq_data = [
        {'Q': '관허 폐차장이 아닌 곳에서 폐차 할 경우 불이익이 있나요?', 'A': '관허 폐차장이 아닌 곳(폐차대행업체, 폐차브로커 등)에 폐차를 신청할 경우 정상적으로 말소등록이 되지 않아 차주에게 세금이 계속 부과되는 경우가 있고, 폐차대행업자와의 연락이 두절되어 차를 분실하는 등 여러 피해 사례가 속출하고 있으니 꼭 관허 폐차장에 의뢰하시기 바랍니다.', '출처': '한국 자동차 해체 재활용업 협회'},
        {'Q': '본인이 직접 말소하려면 어떻게 해야 하나요?', 'A': '말소구비서류(폐차인수증명서, 말소등록신청서)를 지참하여 등록관청에 직접 가셔서 말소신청 하시거나 인터넷 자동차민원 대국민포털(http://www.ecar.go.kr) 에서 공인인증서를 이용하여 로그인 하신 후 신청하실 수 있습니다.', '출처': '한국 자동차 해체 재활용업 협회'},
        {'Q': '자동차 보험은 어떻게 처리해야 하나요?', 'A': '말소등록 후 말소사실증명서를 발급 받아 보험회사로부터 남은 보험료를 환급 받거나 새 차로 이전이 가능합니다.', '출처': '한국 자동차 해체 재활용업 협회'},
        {'Q': '폐차가 제대로 됐는지 어떻게 확인하나요?', 'A': '폐차가 처리되었다는 증명서인 폐차인수증명서를 발급받아 확인하시면 됩니다. 만약 말소등록신청대행을 폐차장에 신청하셨다면 말소완료 이후 등록관청에서 말소사실증명서를 발급받아 확인하실 수 있고 인터넷 자동차민원 대국민포털(http://www.ecar.go.kr) 에서도 확인 가능합니다. ', '출처': '한국 자동차 해체 재활용업 협회'},
        {'Q': '본인이 차주가 아닌 경우 어떻게 폐차하나요?', 'A': '폐차 시 본인이 아닌 경우 차량등록증/차주 인감증명서/대리인 신분증 이 필요합니다.', '출처': '한국 자동차 해체 재활용업 협회'},
        {'Q': '폐차 할 수 있는 지역이 정해져 있나요?', 'A': '폐차는 전 지역에서 가능하니 계신 곳 가까운 관허 폐차장에 문의하시면 됩니다.', '출처': '한국 자동차 해체 재활용업 협회'}
    ]
    
    # st.expander를 사용하여 질문 목록을 표시하고, 열리면 답변이 보이게 합니다.
    if faq_data:
        for i, item in enumerate(faq_data):
            with st.expander(f"**Q{i+1}.** {item['Q']}"):
                st.markdown(f"**A.** {item['A']}")
                st.caption(f"**출처:** {item['출처']}")
    else:
        st.warning("현재 제공 가능한 FAQ 목록이 없습니다.")


# 4. 메인 라우팅 (기존과 동일)
if menu == '폐차장 조회':
    show_scrapyard_finder()
elif menu == 'FAQ 검색 시스템':
    show_faq_system()