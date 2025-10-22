import pymysql;

"""
Author: 박수빈
Date: 2025-10-22
Description: 공용함수
"""

# -------------------------------
# DB 연결 공통 함수
# TODO 이선님 DB 생성 후, 아래 함수 변수 변경 필요.
# -------------------------------
def get_connection():
    return pymysql.connect(
        host=DB_CONFIG["host"],
        user=DB_CONFIG["user"],
        password=DB_CONFIG["password"],
        database=DB_CONFIG["database"],
        port=DB_CONFIG["port"],
        cursorclass=pymysql.cursors.DictCursor,
    )
    
    