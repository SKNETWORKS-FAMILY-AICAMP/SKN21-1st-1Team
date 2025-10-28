"""
Author      : 신지용
Date        : 2025-10-22
Last Update : 2025-10-23
Description : CSV 파일을 읽고, 주소를 파싱하여 지역/하위지역/코드 컬럼을 추가한 DataFrame을 생성
File Role   : CSV → pandas DataFrame 변환 및 address_parser 연동
"""

import pandas as pd
from address_parser import parse_address

def read_and_parse_csv(csv_path: str):
    """
    CSV 파일을 읽어서 주소를 파싱하고, 지역명 및 지역 코드를 생성하는 함수

    Args:
        csv_path (str): 읽어올 CSV 파일 경로

    Returns:
        pd.DataFrame: 지역명(REGION_NAME), 하위지역명(SUBREGION_NAME), 지역코드(REGION_CODE)가 포함된 DataFrame
    """

    df = pd.read_csv(csv_path)
    
    # 주소 파싱
    df["REGION_NAME"], df["SUBREGION_NAME"] = zip(*df["ADDRESS"].map(parse_address))

    # None → 기본값 처리 (파싱 실패 방지)
    df["REGION_NAME"] = df["REGION_NAME"].fillna("서울특별시")

    # 지역 코드 매핑 딕셔너리 (서울, 경기, 인천)
    region_code_map = {
        "서울": "02",
        "서울시": "02",
        "서울특별시": "02",
        "경기": "01",
        "경기도": "01",
        "인천": "11",
        "인천시": "11",
        "인천광역시": "11",
    }

    # REGION_CODE 컬럼 생성 (없을 경우 기본값 "00")
    df["REGION_CODE"] = df["REGION_NAME"].map(region_code_map).fillna("00")

    # 🧾 디버깅용 진단 로그 (파싱 실패 or 코드 누락 행)
    for _, row in df.iterrows():
        if row["REGION_CODE"] == "00" or row["SUBREGION_NAME"] is None:
            print(f"⚠️ 파싱 실패 또는 코드 누락: {row['ADDRESS']} → {row['REGION_NAME']}, {row['SUBREGION_NAME']}")

    return df
