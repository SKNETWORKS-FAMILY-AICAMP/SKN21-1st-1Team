import streamlit as st
import pandas as pd
import json
import os
from io import BytesIO
import plotly.express as px

st.set_page_config(page_title="🚘 폐차 실적 데이터", layout="wide")
st.title("📊 연도별 폐차 실적 데이터")

DATA_DIR = "./data"

# -----------------------------
# JSON → DataFrame 변환
# -----------------------------
def json_to_dataframe(json_path):
    with open(json_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    # ✅ JSON 구조 자동 정리
    # case1: dict인 경우 내부 리스트 추출
    if isinstance(data, dict):
        if "data" in data:
            data = data["data"]
        elif "records" in data:
            data = data["records"]
        else:
            data = list(data.values())

    # case2: list인데 안에 또 list가 있으면 평탄화 (이중 리스트)
    elif isinstance(data, list):
        while len(data) == 1 and isinstance(data[0], list):
            data = data[0]

    # 리스트 안의 비딕셔너리 제거
    data = [d for d in data if isinstance(d, dict)]

    records = []

    for item in data:
        if not isinstance(item, dict):
            continue

        region = item.get("지역", "미상")
        total_sum = item.get("합계", 0)

        # 합계 자동 계산
        if not total_sum:
            total_sum = 0
            for v in item.values():
                if isinstance(v, dict):
                    for sub in v.values():
                        if isinstance(sub, dict):
                            total_sum += sub.get("합계", 0)

        # 하위 구조 변환
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

# -----------------------------
# 엑셀 변환 함수
# -----------------------------
def to_excel(df):
    output = BytesIO()
    with pd.ExcelWriter(output, engine="openpyxl") as writer:
        df.to_excel(writer, index=False, sheet_name="폐차 실적")
    return output.getvalue()


# -----------------------------
# Streamlit UI
# -----------------------------
json_files = [f for f in os.listdir(DATA_DIR) if f.endswith(".json")]
json_files.sort()

if not json_files:
    st.warning("⚠ data 폴더에 JSON 파일이 없습니다.")
    st.stop()

# --- 연도 선택 ---
selected_year = st.sidebar.selectbox("📅 연도 선택", json_files, index=len(json_files) - 1)
selected_path = os.path.join(DATA_DIR, selected_year)

# --- 데이터 표시 ---
try:
    df = json_to_dataframe(selected_path)

    st.markdown(f"### 📘 {selected_year.replace('.json','')} 데이터")
    st.dataframe(df, use_container_width=True, height=500)

    # --- 다운로드 버튼 ---
    excel_data = to_excel(df)
    st.download_button(
        label="💾 엑셀 다운로드",
        data=excel_data,
        file_name=f"{selected_year.replace('.json','')}.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    )

    st.markdown("---")

    # -----------------------------
    # 📊 시각화 ① 지역별 합계 바 차트
    # -----------------------------
    st.subheader("📈 지역별 폐차 실적 합계")

    region_sum = (
        df.groupby("지역", as_index=False)["지역합계"]
        .mean()
        .sort_values("지역합계", ascending=False)
    )

    fig_region = px.bar(
        region_sum,
        x="지역",
        y="지역합계",
        text="지역합계",
        color="지역합계",
        color_continuous_scale="Blues",
        title=f"{selected_year.replace('.json','')} 지역별 합계",
    )
    fig_region.update_traces(texttemplate="%{text:,}", textposition="outside")
    st.plotly_chart(fig_region, use_container_width=True)

    # -----------------------------
    # 📊 시각화 ② 차종별 비율 파이차트
    # -----------------------------
    st.subheader("🥧 차종별 비율")

    vehicle_sum = df.groupby("차종")["합계"].sum().reset_index()

    fig_pie = px.pie(
        vehicle_sum,
        names="차종",
        values="합계",
        color_discrete_sequence=px.colors.sequential.PuBu,
        title=f"{selected_year.replace('.json','')} 차종별 비율",
    )
    fig_pie.update_traces(textinfo="percent+label")
    st.plotly_chart(fig_pie, use_container_width=True)

except Exception as e:
    st.error(f"❌ 변환 중 오류 발생: {e}")
