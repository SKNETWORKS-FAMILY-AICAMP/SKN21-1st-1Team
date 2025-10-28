"""
Author      : 신지용 
Date        : 2025-10-23
Description : MySQL 연결 및 FAQ 테이블 생성, 데이터 INSERT 관리
File Role   : FAQ_INFO 테이블 초기화 및 데이터 저장 기능 담당
"""

import pymysql
import pandas as pd
import numpy as np
from db_config import DB_CONFIG

def recreate_faq_table():
    """
    🧱 FAQ_INFO 테이블을 매 실행 시 새로 생성하는 함수

    기능:
        - 기존 FAQ_INFO 테이블 삭제 (DROP)
        - 새 스키마 구조로 테이블 재생성

    Raises:
        pymysql.MySQLError: DB 연결 또는 SQL 실행 오류 발생 시
    """
    conn = pymysql.connect(**DB_CONFIG)
    cursor = conn.cursor()

    # 기존 테이블 삭제
    cursor.execute("DROP TABLE IF EXISTS FAQ_INFO;")

    # 새로운 테이블 생성
    create_sql = """
    CREATE TABLE FAQ_INFO ( 
        id INT AUTO_INCREMENT PRIMARY KEY,
        question TEXT,
        answer TEXT
    ) DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
    """
    cursor.execute(create_sql)
    conn.commit()
    conn.close()
    print("🧱 FAQ_INFO 테이블 재생성 완료")


def save_faq_to_db(df):
    """
    💾 DataFrame 데이터를 FAQ_INFO 테이블에 삽입하는 함수

    Args:
        df (pd.DataFrame): DB에 삽입할 FAQ 데이터  
            (필수 컬럼: QUESTION, ANSWER)

    Raises:
        KeyError: 필수 컬럼이 DataFrame에 존재하지 않을 경우
        pymysql.MySQLError: DB 연결 또는 INSERT 중 오류 발생 시
    """
    df = df.replace({np.nan: None})

    conn = pymysql.connect(**DB_CONFIG)
    cursor = conn.cursor()

    insert_sql = """
    INSERT INTO FAQ_INFO (question, answer)
    VALUES (%s, %s);
    """

    for _, row in df.iterrows():
        cursor.execute(insert_sql, (row["QUESTION"], row["ANSWER"]))

    conn.commit()
    conn.close()
    print(f"✅ {len(df)}개의 FAQ 데이터가 새 테이블에 삽입되었습니다.")
