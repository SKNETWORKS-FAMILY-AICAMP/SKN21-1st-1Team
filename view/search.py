"""
Author: 문지영 / 신지용 (병합)
Date: 2025-10-27 (최종 수정일)
Description: 주석 삭제
"""
import sys
from pathlib import Path
PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.append(str(PROJECT_ROOT)) 
import streamlit.components.v1 as components 
import plotly.express as px
from pathlib import Path
import streamlit as st
import pandas as pd
import urllib.parse
import math, requests
import json
import os
from io import BytesIO
from utils.path_manager import NEWS_CSV

API_BASE_URL = "http://127.0.0.1:5000"
API_SCRAPYARD = f"{API_BASE_URL}/scrapyards"
API_FAQ_URL = f"{API_BASE_URL}/faqs"
API_SUBREGIONS_URL = f"{API_BASE_URL}/subregions" 
API_LOGIN_URL = f"{API_BASE_URL}/login"
API_REGISTER_URL = f"{API_BASE_URL}/register"
API_WITHDRAW_URL = f"{API_BASE_URL}/withdraw"

REGION_CODE_MAP = {"서울": "02", "경기": "01", "인천": "11"}  

MENU_ITEMS_WITH_EMOJI = [
    ('🏠 홈', '홈'),
    ('🔎 폐차장 조회', '폐차장 조회'),
    ('❓ FAQ 검색 시스템', 'FAQ 검색 시스템'),
    ('📈 실적 데이터', '실적 데이터'),
    ('📰 카드뉴스', '카드뉴스')
]

def handle_api_login(username, password):
    """백엔드 API로 로그인을 시도합니다."""
    try:
        response = requests.post(API_LOGIN_URL, json={"username": username, "password": password})
        return response.json()
    except requests.exceptions.RequestException as e:
        return {"success": False, "message": f"서버 연결 오류: {e}"}

def handle_api_register(username, password):
    """백엔드 API로 회원가입을 시도합니다."""
    try:
        response = requests.post(API_REGISTER_URL, json={"username": username, "password": password})
        return response.json()
    except requests.exceptions.RequestException as e:
        return {"success": False, "message": f"서버 연결 오류: {e}"}

def show_login_page():
    """로그인 및 회원가입 UI를 탭으로 표시합니다."""
    st.set_page_config(
        page_title="로그인",
        page_icon="🔒",
        layout="centered"
    )
    st.title("🔒 수도권 폐차 정보 통합 시스템")

    tab1, tab2 = st.tabs(["로그인", "회원가입"])

    with tab1:
        st.subheader("로그인")
        with st.form("login_form"):
            login_username = st.text_input("아이디 (Username)", key="login_user")
            login_password = st.text_input("비밀번호 (Password)", type="password", key="login_pass")
            login_submitted = st.form_submit_button("로그인")

            if login_submitted:
                if not login_username or not login_password:
                    st.error("아이디와 비밀번호를 모두 입력하세요.")
                else:
                    result = handle_api_login(login_username, login_password)
                    if result.get("success"):
                        st.session_state.logged_in = True
                        st.session_state.username = login_username
                        st.session_state.show_welcome_popup = True 
                        st.rerun()
                    else:
                        st.error(result.get("message", "로그인에 실패했습니다."))

    with tab2:
        st.subheader("회원가입")
        with st.form("register_form"):
            reg_username = st.text_input("사용할 아이디", key="reg_user")
            reg_password = st.text_input("사용할 비밀번호", type="password", key="reg_pass")
            reg_password_confirm = st.text_input("비밀번호 확인", type="password", key="reg_pass_confirm")
            reg_submitted = st.form_submit_button("가입하기")

            if reg_submitted:
                if not reg_username or not reg_password or not reg_password_confirm:
                    st.error("모든 항목을 입력하세요.")
                elif reg_password != reg_password_confirm:
                    st.error("비밀번호가 일치하지 않습니다.")
                else:
                    result = handle_api_register(reg_username, reg_password)
                    if result.get("success"):
                        st.session_state.logged_in = True
                        st.session_state.username = reg_username
                        st.session_state.show_welcome_popup = True
                        st.rerun() 
                    else:
                        st.error(result.get("message", "회원가입에 실패했습니다."))

def show_main_app():
    """로그인 성공 시, 기존의 메인 애플리케이션을 표시합니다."""

    st.set_page_config(
        page_title="수도권 폐차장 조회 및 FAQ 시스템",
        page_icon="🚙",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    if st.session_state.show_welcome_popup:
        username = st.session_state.get("username", "사용자")
        st.success(f"🎉 환영합니다, {username} 님! 좋은 하루 되세요~", icon="👋")
        st.balloons()
        st.session_state.show_welcome_popup = False

    if st.sidebar.button("로그아웃 🔒", key="logout_btn_top", use_container_width=True):
        st.session_state.logged_in = False
        st.session_state.username = None 
        st.session_state.show_welcome_popup = False 
        st.rerun() 

    st.markdown("""
    <style>
    /* ... (기존 search.py의 CSS 스타일과 동일) ... */
    /* ----------------- 모든 Streamlit 버튼의 기본 스타일 (미색 계열) ----------------- */
    div.stButton > button:first-child {
        color: #31333f; /* 글자색 검은색 */
        background-color: #f0f2f6; /* 미색 계열 배경 */
        border-radius: 5px;
        padding: 8px 16px;
        font-weight: bold;
        border: 1px solid #d3d3d3; /* 옅은 테두리 */
        margin-top: 10px; /* 모든 버튼에 기본 여백 적용 */
        transition: all 0.2s; /* 호버 애니메이션을 위한 트랜지션 추가 */
    }
    /* ----------------- 검색 버튼 스타일 (파란색 강제 유지) ----------------- */
    .blue-search-button div.stButton > button:first-child {
        color: white !important;
        background-color: #1158e0 !important; 
        border: 1px solid #1158e0 !important;
        font-weight: bold !important;
    }
    /* ----------------- 사이드바 일반 버튼 스타일 (선택되지 않은) ----------------- */
    .sidebar div.stButton > button:first-child {
        width: 100%; 
        margin-bottom: 5px;
        text-align: left; 
        font-weight: normal;
        padding: 8px 10px; 
        margin-top: 5px; /* 사이드바 버튼은 상단 마진을 줄임 */
    }
    /* ----------------- 사이드바 버튼 스타일 (선택됨) ----------------- */
    .selected-menu-btn div.stButton > button:first-child {
        background-color: #1158e0 !important; /* 파란색 강조색 */
        color: white !important; /* 텍스트 흰색 */
        border: 1px solid #1158e0 !important;
        font-weight: bold;
    }
    /* ❗️ [조건 2] 로그아웃 버튼 스타일 (상단에 배치되므로 다른 버튼과 스타일 통일) */
    [data-testid="stSidebar"] div.stButton > button[key="logout_btn_top"] {
        width: 100%; 
        margin-bottom: 15px; /* 제목과 간격 띄우기 */
        text-align: left; 
        font-weight: bold;
        padding: 8px 10px; 
        margin-top: 5px;
        color: #31333f;
        background-color: #f0f2f6;
        border: 1px solid #d3d3d3;
    }
    [data-testid="stSidebar"] div.stButton > button[key="logout_btn_top"]:hover {
        color: white !important;
        background-color: #1158e0 !important;
    }
                
    /* ----------------- 경고/정보 스타일 ----------------- */
    div[data-testid="stAlert"] div[role="alert"] {
        text-align: center; 
        padding-top: 15px;
        padding-bottom: 15px;
    }
                
    .stVerticalBlock .st-emotion-cache-wfksaw.e196pkbe2 {
    align-items: center;
}     
    </style>
    """, unsafe_allow_html=True)


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
            return [] 
        
        try:
            params = {"region": region_code}
            resp = requests.get(API_SUBREGIONS_URL, params=params, timeout=timeout)
            resp.raise_for_status()
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

    def create_kakaomap_url(address):
        """주소를 카카오맵 검색 URL로 인코딩하여 새 창으로 여는 URL을 반환합니다."""
        base_url = "https://map.kakao.com/"
        encoded_address = urllib.parse.quote(address)
        return f"{base_url}?q={encoded_address}"

    def get_kakao_map_iframe_url(address):
        """주소를 카카오맵 iframe 임베딩용 URL로 인코딩하여 반환합니다. (검색창 숨김)"""
        encoded_address = urllib.parse.quote(address)
        return f"https://map.kakao.com/?q={encoded_address}&map_type=TYPE_MAP&src=internal"

    def get_scrapyard_list_with_address(selected_area, selected_district):
        """
        Flask API로 폐차장 데이터를 요청하여 DataFrame으로 반환
        """
        try:
            params = {}
            if selected_area not in ("", "전체"):
                params["region"] = REGION_CODE_MAP.get(selected_area) 
            if selected_district not in ("", "전체"):
                params["subregion"] = selected_district

            response = requests.get(API_SCRAPYARD, params=params, timeout=5)
            response.raise_for_status()

            data = response.json()
            if not data:
                st.warning("조건에 맞는 폐차장 데이터가 없습니다.")
                return pd.DataFrame()

            df = pd.DataFrame(data)

            df.rename(columns={
                "SY_NAME": "업체명",
                "ADDRESS": "주소",
                "CONTACT_NUMBER": "연락처",
                "REGION_CODE": "지역코드",
                "SUBREGION_NAME": "세부지역",
                "SY_ID": "ID"
            }, inplace=True)

            return df[['ID', '업체명', '주소', '연락처']] 

        except requests.exceptions.RequestException as e:
            st.error(f"🚨 Flask 서버 통신 오류: {e}")
            return pd.DataFrame()


    def perform_search_and_reset():
        """검색을 수행하고 페이지 및 지도 세션 상태를 초기화합니다."""
        selected_area = st.session_state.area_select 
        selected_district = st.session_state.district_select 
        
        st.session_state.current_page = 1
        st.session_state.map_info = {'address': None, 'url': None}
        
        result_df = get_scrapyard_list_with_address(selected_area, selected_district)
        st.session_state.last_search_df = result_df

    def set_menu(menu_name):
        """사이드바 메뉴 선택 시 세션 상태를 업데이트하고 페이지를 새로고침합니다."""
        st.session_state.menu_selection = menu_name
        st.session_state.map_info = {'address': None, 'url': None} 

    st.sidebar.title("⚙️ INFORMATION")
    for label_with_emoji, item in MENU_ITEMS_WITH_EMOJI:
        if st.session_state.menu_selection == item:
            st.sidebar.markdown(f'<div class="selected-menu-btn">', unsafe_allow_html=True)
            st.sidebar.button(
                label_with_emoji, 
                key=f"sidebar_btn_{item}", 
                on_click=set_menu, 
                args=(item,),
                use_container_width=True
            )
            st.sidebar.markdown('</div>', unsafe_allow_html=True)
        else:
            st.sidebar.button(
                label_with_emoji, 
                key=f"sidebar_btn_{item}", 
                on_click=set_menu, 
                args=(item,),
                use_container_width=True
            )
        
    menu = st.session_state.menu_selection

    def show_scrapyard_finder():
        """ 폐차장 조회 페이지 (지도 임베드 기능 통합) """
        st.header ("🚙 수도권 폐차장 조회")
        st.write("원하는 지역과 세부 지역을 선택한 후 검색하세요.")

        col1, col2, col3 = st.columns([1, 1, 0.4])
        with col1:
            st.selectbox(
                "지역별 검색 (시/도)",
                ['전체', '서울', '경기', '인천'],
                index = ['전체', '서울', '경기', '인천'].index(st.session_state.area_select),
                key="area_select",
                on_change=lambda: st.session_state.update(district_select='전체')
            )
        
        selected_region_name = st.session_state.area_select
        selected_region_code = REGION_CODE_MAP.get(selected_region_name)
        
        detail_options_from_db = load_subregions_from_api(selected_region_code) 
        detail_options = ['전체'] + detail_options_from_db

        with col2:
            current_district = st.session_state.district_select
            if current_district not in detail_options:
                current_district = '전체'
                st.session_state.district_select = '전체'
            
            st.selectbox(
                f"'{st.session_state.area_select}'의 세부 지역 검색 (구/시)",
                detail_options,
                index=detail_options.index(current_district),
                key="district_select"
            )
            
        with col3:
            st.markdown('<div class="blue-search-button">', unsafe_allow_html=True)
            st.button("검색", on_click=perform_search_and_reset, key="search_button_widget", use_container_width=True) 
            st.markdown('</div>', unsafe_allow_html=True)    
                            
        if not st.session_state.last_search_df.empty:
            
            result_df = st.session_state.last_search_df
            total_rows = len(result_df)
            page_size = 5
            total_pages = math.ceil(total_rows / page_size)
            current_page = st.session_state.current_page

            st.subheader(f"🔍 조회 결과 (**{total_rows}**건)")

            start_row = (current_page - 1) * page_size
            end_row = start_row + page_size
            paginated_df = result_df.iloc[start_row:end_row].copy()

            header_cols = st.columns([2.5, 3.5, 1.5, 2.0]) 
            header_cols[0].markdown('**업체명**')
            header_cols[1].markdown('**주소**')
            header_cols[2].markdown('**연락처**')
            header_cols[3].markdown('**지도**')

            st.markdown('<hr class="header-divider"/>', unsafe_allow_html=True) 

            for index, row in paginated_df.iterrows():
                row_cols = st.columns([2.5, 3.5, 1.5, 2.0])
                
                row_cols[0].markdown(f"**{row['업체명']}**", unsafe_allow_html=True)
                row_cols[1].markdown(row['주소'])
                row_cols[2].markdown(row['연락처'])

                with row_cols[3]:
                    if st.button("🗺️ 지도 보기", key=f"mapbtn{row['ID']}", use_container_width=True):
                        st.session_state.map_info['address'] = row['주소']
                        st.session_state.map_info['url'] = get_kakao_map_iframe_url(row['주소'])
                        st.rerun()
                
                st.markdown('<hr class="row-divider"/>', unsafe_allow_html=True)
            
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
            st.info("검색 조건을 선택하고 '검색' 버튼을 눌러주세요.")

        if st.session_state.map_info['address']:
            st.markdown("---")
            st.subheader(f"🗺️ 위치 확인: {st.session_state.map_info['address']}")
            map_url = st.session_state.map_info['url']
            components.html(
                f"""
                <iframe 
                    width="100%" height="500" frameborder="0" scrolling="no" 
                    marginwidth="0" marginheight="0" src="{map_url}">
                </iframe>
                """,
                height=520, 
            )

    def show_faq_system():
        st.header("❓ 폐차 관련 자주 묻는 질문 (FAQ)")
        st.write("자주 묻는 질문 목록입니다. 질문을 클릭하시면 답변을 확인할 수 있습니다.")

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

        col1, col2 = st.columns([0.82, 0.18])
        with col1:
            query = st.text_input("", placeholder="검색어를 입력하세요").strip()
        with col2:
            st.markdown(
                """
        <style>
        /* 이 블록 내부(div id="search-btn-area")에 있는 Streamlit 버튼만 스타일링 */
        #search-btn-area .stButton>button {
            background-color: #1158e0 !important;
            color: #ffffff !important;
            height: 44px !important;
            border-radius: 8px !important;
            font-weight: 600 !important;
            border: none !important;
            box-shadow: none !important;
        }
        #search-btn-area .stButton>button:focus {
            outline: none !important;
            box-shadow: none !important;
        }
        </style>
        <div id="search-btn-area"></div>
        """,
                unsafe_allow_html=True,
            )
            search_clicked = st.button("검색", key="search_button")

        filtered = df
        if (search_clicked if 'search_clicked' in locals() else False) or query:
            q_lower = query.lower()
            mask = (
                df.get("Q", "").astype(str).str.lower().str.contains(q_lower, na=False)
                | df.get("A", "").astype(str).str.lower().str.contains(q_lower, na=False)
                | df.get("출처", "").astype(str).str.lower().str.contains(q_lower, na=False)
            )
            filtered = df[mask]
            if filtered.empty:
                st.info(f"'{query}'(을)를 포함하는 FAQ 항목이 없습니다.")
                return

        st.write("")
        st.write("---")
        st.write("")

        for i, row in filtered.reset_index(drop=True).iterrows():
            q = row.get("Q", "")
            a = row.get("A", "")
            src = row.get("출처", "")
            with st.expander(f"Q{i+1}. {q}"):
                st.markdown(a)
                if src:
                    st.caption(f"출처: {src}")
                st.write("")
            st.write("")


    def json_to_dataframe(json_path):
        with open(json_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        if isinstance(data, dict):
            if "data" in data:
                data = data["data"]
            elif "records" in data:
                data = data["records"]
            else:
                data = list(data.values())
        elif isinstance(data, list):
            while len(data) == 1 and isinstance(data[0], list):
                data = data[0]
        data = [d for d in data if isinstance(d, dict)]
        records = []
        for item in data:
            if not isinstance(item, dict):
                continue
            region = item.get("지역", "미상")
            total_sum = item.get("합계", 0)
            if not total_sum:
                total_sum = 0
                for v in item.values():
                    if isinstance(v, dict):
                        for sub in v.values():
                            if isinstance(sub, dict):
                                total_sum += sub.get("합계", 0)
            for vehicle, details in item.items():
                if vehicle in ["지역", "합계"]:
                    continue
                for use_type, values in details.items():
                    if not isinstance(values, dict):
                        continue
                    record = {
                        "지역": region,
                        "차종": vehicle,
                        "용도": use_type,
                        "자도": values.get("자도", 0),
                        "타도": values.get("타도", 0),
                        "합계": values.get("합계", 0),
                        "지역합계": total_sum,
                    }
                    records.append(record)
        return pd.DataFrame(records)

    def to_excel(df):
        """DataFrame을 엑셀 파일 형태로 변환합니다."""
        output = BytesIO()
        with pd.ExcelWriter(output, engine="openpyxl") as writer: 
            df.to_excel(writer, index=False, sheet_name="폐차 실적")
        return output.getvalue()


    def show_performance_data():
        """ 실적 데이터 조회 및 시각화 페이지 """
        
        DATA_DIR = "./data" 

        json_files = []
        try:
            json_files = [f for f in os.listdir(DATA_DIR) if f.endswith(".json")]
            json_files.sort()
        except FileNotFoundError:
            st.error(f"❌ '{DATA_DIR}' 폴더를 찾을 수 없습니다. JSON 파일을 이 폴더에 넣어주세요.")
            return

        if not json_files:
            st.warning(f"⚠ {DATA_DIR} 폴더에 JSON 파일이 없습니다.")
            return
        
        st.title("📊 연도별 폐차 실적 데이터") 
        
        if 'performance_year_select' not in st.session_state or st.session_state.performance_year_select not in json_files:
            st.session_state.performance_year_select = json_files[-1] 

        col_data_title, col_select = st.columns([0.8, 0.2]) 
        selected_year_display = st.session_state.performance_year_select.replace('.json', '')

        with col_data_title:
            st.markdown(f"### 📘 {selected_year_display} 데이터")
        with col_select: 
            st.selectbox(
                "연도 선택", 
                json_files, 
                key="performance_year_select",
                label_visibility="hidden", 
            )
        
        selected_path = os.path.join(DATA_DIR, st.session_state.performance_year_select)
        st.markdown("---") 

        try:
            df = json_to_dataframe(selected_path) 
            st.dataframe(df, use_container_width=True, height=500)
            excel_data = to_excel(df)
            st.download_button(
                label="💾 엑셀 다운로드",
                data=excel_data,
                file_name=f"{selected_year_display}.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            )
            st.markdown("---")
            
            st.subheader("📈 지역별 폐차 실적 합계")
            region_sum = (
                df.groupby("지역", as_index=False)["지역합계"]
                .mean()
                .sort_values("지역합계", ascending=False)
            )
            fig_region = px.bar(
                region_sum, x="지역", y="지역합계", text="지역합계",
                color="지역합계", color_continuous_scale="Blues",
                title=f"{selected_year_display} 지역별 합계",
            )
            fig_region.update_traces(texttemplate="%{text:,}", textposition="outside")
            st.plotly_chart(fig_region, use_container_width=True)

            st.subheader("🥧 차종별 비율")
            vehicle_sum = df.groupby("차종")["합계"].sum().reset_index()
            fig_pie = px.pie(
                vehicle_sum, names="차종", values="합계",
                color_discrete_sequence=px.colors.sequential.PuBu,
                title=f"{selected_year_display} 차종별 비율",
            )
            fig_pie.update_traces(textinfo="percent+label")
            st.plotly_chart(fig_pie, use_container_width=True)

        except Exception as e:
            st.error(f"❌ 데이터 처리 중 오류 발생: {e}")


    def show_news_cards():
        """
        Streamlit에서 카드뉴스를 CSV 기반으로 표시하는 함수
        """
        st.header("📰 폐차 관련 뉴스")
        st.write("카드를 클릭하면 뉴스 원문 페이지로 이동합니다.")

        try:
            df = pd.read_csv(NEWS_CSV, encoding='utf-8-sig')
            df.columns = df.columns.str.strip()
            if df.empty:
                st.warning("CSV에 뉴스 데이터가 없습니다.")
                return
            
            required_cols = ['title', 'snippet', 'link', 'image']
            for col in required_cols:
                if col not in df.columns:
                    st.error(f"CSV에 필수 컬럼 '{col}'가 없습니다. (현재 컬럼: {df.columns.tolist()})")
                    return

            html_content = """
            <style>
            /* ... (카드 CSS 동일) ... */
            .grid {
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
                gap: 20px;
            }
            .card {
                background: white; border-radius: 16px; padding: 16px;
                box-shadow: 0 3px 10px rgba(0,0,0,0.1);
                transition: transform 0.2s ease; cursor: pointer;
                overflow: hidden;
            }
            .card:hover { transform: translateY(-5px); background-color: #1158e0; color: white; }
            .card img {
                width: 100%; height: 150px; object-fit: cover;
                border-radius: 10px; margin-bottom: 10px;
                referrerpolicy: no-referrer;
            }
            .title { font-weight: bold; font-size: 18px; margin-bottom: 8px; color: #31333f; }
            .snippet { color: #555; font-size: 14px; }
            .card:hover .snippet, .card:hover .title { color: white !important; }
            </style>
            <div class="grid">
            """

            for _, row in df.iterrows():
                title = row.get('title', '제목 없음')
                snippet = row.get('snippet', '요약 없음')
                link = row.get('link', '#')
                image = row.get('image', 'https://via.placeholder.com/300x150?text=No+Image')

                card_html = f"""
                <div class="card" onclick="window.open('{link}', '_blank')">
                    <img src="{image}" alt="news image" referrerpolicy="no-referrer">
                    <div class="title">{title}</div>
                    <div class="snippet">{snippet}</div>
                </div>
                """
                html_content += card_html
            html_content += "</div>"
            st.components.v1.html(html_content, height=800, scrolling=True)

        except FileNotFoundError:
            st.error(f"CSV 파일 '{NEWS_CSV}'을(를) 찾을 수 없습니다.")
        except Exception as e:
            st.error(f"뉴스 카드 표시 중 오류 발생: {e}")


    if menu == '홈':
        st.title("🏠 수도권 폐차 정보 통합 시스템")
        
        st.header("📊 수도권 폐차 현황 (최신 데이터 기반)")
        col_stat1, col_stat2, col_stat3 = st.columns(3)

        total_scrapyards = 66  
        latest_year = "2025년 9월" 
        top_region = "경기"   

        with col_stat1:
            st.metric(label="등록된 폐차장 수", value=f"{total_scrapyards} 곳", delta="정식 인증 업체")
            
        with col_stat2:
            st.metric(label=f"최신 실적 연도", value=f"{latest_year}", delta="데이터 투명성 확보")

        with col_stat3:
            st.metric(label=f"폐차 최대 지역", value=f"{top_region} 지역", delta="최근 실적 기준")
            
        st.write("---") 

        st.header("✨ 시스템 개요 및 주요 기능")
        st.markdown("""
            복잡한 폐차 과정을 쉽고 투명하게! 
            본 시스템은 **서울, 경기, 인천 지역**의 **정식 등록된 폐차 정보**를 통합하여 사용자에게 제공합니다.
        """)
        
        col_1, col_2, col_3 = st.columns(3)
        
        with col_1:
            st.subheader("1. 폐차장 위치 조회 🔎")
            st.info("실시간 위치 기반 검색 및 지도 연동 기능을 통해 가장 가까운 폐차장을 찾고 연락하세요.")
            st.markdown('<div class="home-link-button">', unsafe_allow_html=True)
            if st.button("🔎 폐차장 조회 바로가기", key="home_to_scrapyard_btn", use_container_width=True):
                set_menu('폐차장 조회')
                st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)
            
        with col_2:
            st.subheader("2. FAQ 검색 시스템 ❓")
            st.info("폐차 절차, 필요 서류, 보조금 등 자주 묻는 질문에 대한 정확한 답변을 제공합니다.")
            st.markdown('<div class="home-link-button">', unsafe_allow_html=True)
            if st.button("❓ FAQ 검색 바로가기", key="home_to_faq_btn", use_container_width=True):
                set_menu('FAQ 검색 시스템')
                st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)


        with col_3:
            st.subheader("3. 실적 데이터 📈")
            st.info("지역별/연도별 폐차 실적 데이터를 시각화 자료로 제공합니다.")
            st.markdown('<div class="home-link-button">', unsafe_allow_html=True)
            if st.button("📈 실적 데이터 바로가기", key="home_to_performance_btn", use_container_width=True):
                set_menu('실적 데이터')
                st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)


        st.write("---")

        st.header("🔍 어떤 폐차를 진행해야 할까요?")
        st.write("차량 상태와 목적에 따라 필요한 절차가 다릅니다. 자주 찾는 폐차 유형을 확인해보세요.")

        type_col1, type_col2 = st.columns(2)

        with type_col1:
            st.subheader("✅ 일반 폐차 (가장 흔함)")
            st.success("차량에 압류나 저당이 **없는** 경우")
            st.caption("차량 인수 후 24시간 이내 말소 등록 완료. 간편하고 빠르게 진행 가능합니다. 자세한 절차는 FAQ에서 확인하세요.")

        with type_col2:
            st.subheader("⚠️ 압류/저당 폐차 (차령초과)")
            st.warning("차량에 **압류나 저당이 남아있는** 경우")
            st.caption("특정 연식 기준(차령) 초과 시 압류 해제 없이 폐차(차령초과 말소) 가능. 완료까지 약 2개월 소요됩니다.")
        
        st.write("---")

        st.header("✅ 폐차 진행 과정 (간편 가이드)")
        
        col_a, col_b, col_c = st.columns(3)
        
        with col_a:
            st.metric("STEP 1. 신청 및 상담", "원하는 폐차장 선택", "전화/방문 접수")
            st.caption("폐차장 조회 메뉴에서 업체를 선택하고 폐차를 신청합니다.")
            
        with col_b:
            st.metric("STEP 2. 차량 인계 및 서류", "차량 견인 및 서류 제출", "등록증, 신분증 사본")
            st.caption("차량을 인계하고 필수 서류를 폐차장에 전달합니다.")
            
        with col_c:
            st.metric("STEP 3. 말소 및 대금 수령", "말소 등록 및 대금 수령", "24시간 내 완료")
            st.caption("폐차장이 말소 등록 후 말소증을 전달하고 대금을 지급합니다.")
            

    elif menu == '폐차장 조회':
        show_scrapyard_finder()
    elif menu == 'FAQ 검색 시스템':
        show_faq_system()
    elif menu == '실적 데이터':
        show_performance_data()
    elif menu == '카드뉴스':
        show_news_cards()
 

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "show_welcome_popup" not in st.session_state:
    st.session_state.show_welcome_popup = False
if "username" not in st.session_state:
    st.session_state.username = None 
if 'menu_selection' not in st.session_state:
    st.session_state.menu_selection = '홈'
if 'current_page' not in st.session_state:
    st.session_state.current_page = 1
if 'last_search_df' not in st.session_state:
    st.session_state.last_search_df = pd.DataFrame()
if 'map_info' not in st.session_state:
    st.session_state.map_info = {'address': None, 'url': None}
if 'area_select' not in st.session_state:
    st.session_state.area_select = '전체'
if 'district_select' not in st.session_state:
    st.session_state.district_select = '전체'


if st.session_state.logged_in:
    show_main_app()  
else:
    show_login_page() 