"""
Author      : 신지용 
Date        : 2025-10-22
Last Update : 2025-10-23
Description : MySQL 연결 및 테이블 생성, 데이터 INSERT 관리
File Role   : DB 테이블 초기화 및 데이터 저장 기능 담당
"""


import pymysql
import pandas as pd
import numpy as np
from db_config import DB_CONFIG

def recreate_table():
    """
    🧱 SCRAPYARD_INFO 테이블을 매 실행 시 새로 생성하는 함수

    기능:
        - 기존 테이블이 존재하면 DROP
        - 새로운 스키마 구조로 테이블 재생성

    Raises:
        pymysql.MySQLError: DB 연결 또는 SQL 실행 오류 발생 시
    """

    conn = pymysql.connect(**DB_CONFIG)
    cursor = conn.cursor()

    cursor.execute("DROP TABLE IF EXISTS SCRAPYARD_INFO;")

    create_sql = """
    CREATE TABLE SCRAPYARD_INFO (
        SY_ID BIGINT NOT NULL AUTO_INCREMENT PRIMARY KEY,
        SY_NAME VARCHAR(100) NOT NULL,
        CEO_NAME VARCHAR(50),
        CONTACT_NUMBER VARCHAR(20),
        ADDRESS VARCHAR(255) NOT NULL,
        REGION_CODE VARCHAR(2) NOT NULL,
        SUBREGION_NAME VARCHAR(50) NOT NULL,
        CREATED_AT DATETIME DEFAULT CURRENT_TIMESTAMP
    ) DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
    """
    cursor.execute(create_sql)
    conn.commit()
    conn.close()
    print("🧱 SCRAPYARD_INFO 테이블 재생성 완료")


def save_to_db(df):
    """
    💾 DataFrame 데이터를 SCRAPYARD_INFO 테이블에 삽입하는 함수

    Args:
        df (pd.DataFrame): DB에 삽입할 폐차장 정보 DataFrame  
            (필수 컬럼: SY_NAME, CEO_NAME, CONTACT_NUMBER, ADDRESS, REGION_CODE, SUBREGION_NAME)

    Raises:
        KeyError: 필수 컬럼이 DataFrame에 존재하지 않을 경우
        pymysql.MySQLError: DB 연결 또는 INSERT 중 오류 발생 시
    """
    df = df.replace({np.nan: None})

    conn = pymysql.connect(**DB_CONFIG)
    cursor = conn.cursor()

    insert_sql = """
    INSERT INTO SCRAPYARD_INFO
    (SY_NAME, CEO_NAME, CONTACT_NUMBER, ADDRESS, REGION_CODE, SUBREGION_NAME)
    VALUES (%s, %s, %s, %s, %s, %s);
    """

    for _, row in df.iterrows():
        cursor.execute(insert_sql, (
            row["SY_NAME"],
            row["CEO_NAME"],
            row["CONTACT_NUMBER"],
            row["ADDRESS"],
            row["REGION_CODE"],
            row["SUBREGION_NAME"]
        ))

    conn.commit()
    conn.close()
    print(f"✅ {len(df)}개의 데이터가 새 테이블에 삽입되었습니다.")
