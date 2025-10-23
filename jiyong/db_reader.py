"""
Author      : 신지용
Date        : 2025-10-22
Last Update : 2025-10-23
Description : DB에서 폐차장 데이터 조회 
File Role   : SELECT 쿼리 및 데이터 조회용 
"""

import pymysql
import pandas as pd
from db_config import DB_CONFIG

def get_regions():
    """REGION_CODES 테이블에서 지역 목록 조회"""
    conn = pymysql.connect(**DB_CONFIG)
    query = "SELECT CODE, CODE_NAME FROM REGION_CODES ORDER BY CODE;"
    df = pd.read_sql(query, conn)
    conn.close()
    return df.to_dict(orient="records")

def get_subregions(region_code: str):
    """폐차장 테이블에서 특정 지역 코드의 시군구 목록 조회"""
    conn = pymysql.connect(**DB_CONFIG)
    query = """
        SELECT DISTINCT SUBREGION_NAME
        FROM SCRAPYARD_INFO
        WHERE REGION_CODE = %s
        ORDER BY SUBREGION_NAME;
    """
    df = pd.read_sql(query, conn, params=[region_code])
    conn.close()
    return df["SUBREGION_NAME"].tolist()

def get_scrapyards(region_code: str, subregion: str):
    """특정 시군구의 폐차장 목록 (이름, 주소, 전화번호 등)"""
    conn = pymysql.connect(**DB_CONFIG)
    query = """
        SELECT SY_NAME, CEO_NAME, CONTACT_NUMBER, ADDRESS
        FROM SCRAPYARD_INFO
        WHERE REGION_CODE = %s AND SUBREGION_NAME = %s
        ORDER BY SY_NAME;
    """
    df = pd.read_sql(query, conn, params=[region_code, subregion])
    conn.close()
    return df.to_dict(orient="records")
