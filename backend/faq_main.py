"""
Author      : 신지용
Date        : 2025-10-28
Description : FAQ CSV → MySQL 저장 전체 실행 스크립트
File Role   : FAQ 테이블 초기화 → CSV 로드 → DB 저장 자동 실행
"""

from faq_csv_reader import read_faq_csv
from faq_db_writer import recreate_faq_table, save_faq_to_db

def main():
    """
    🧩 FAQ 데이터 적재 파이프라인 실행 함수

    1. 기존 FAQ_INFO 테이블을 재생성 (DROP + CREATE)
    2. CSV 파일을 읽어 DataFrame으로 로드
    3. 로드된 데이터를 MySQL DB에 INSERT

    Raises:
        Exception: 하위 모듈 실행 중 예외 발생 시 출력
    """
    # 1️⃣ FAQ 테이블 재생성
    recreate_faq_table()
    # 2️⃣ CSV 파일 읽기
    df = read_faq_csv()
    # 3️⃣ DB에 FAQ 데이터 저장
    save_faq_to_db(df)

if __name__ == "__main__":
    main()
