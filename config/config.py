import os

"""
Author: 박수빈
Date: 2025-10-22
Description: 공통 상수 및 변수 작성.
"""

# -------------------------------
# DB 설정 상수
# TODO 이선님이 DB 생성 후, 아래 변수 변경 필요.
# -------------------------------
DB_CONFIG = {
    "host": os.getenv("DB_HOST", "localhost"),
    "user": os.getenv("DB_USER", "root"),
    "password": os.getenv("DB_PASSWORD", "1234"),
    "database": os.getenv("DB_NAME", "testdb"),
    "port": int(os.getenv("DB_PORT", 3306)),
}