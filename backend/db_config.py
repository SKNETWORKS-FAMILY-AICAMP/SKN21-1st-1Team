"""
Author      : 신지용
Date        : 2025-10-28
Description : MySQL 데이터베이스 접속 설정 파일
Usage       : 다른 모듈에서 import 하여 DB 연결 시 사용
"""
# ✅ MySQL 접속 정보 설정
# - host: DB 서버 주소 (로컬 테스트 시 'localhost')
# - user: MySQL 사용자 이름
# - password: MySQL 비밀번호
# - database: 사용할 데이터베이스 이름
# - charset: 한글 인코딩을 위해 'utf8mb4' 사용

DB_CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": "1234",
    "database": "testdb",
    "charset": "utf8mb4"
}
