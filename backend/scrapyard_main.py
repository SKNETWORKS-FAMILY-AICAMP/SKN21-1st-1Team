"""
Author      : 신지용 
Date        : 2025-10-22
Last Update : 2025-10-23
Description : CSV 데이터를 읽어 주소 파싱 및 MySQL DB에 저장하는 메인 실행 스크립트
File Role   : 전체 파이프라인 실행 (CSV → 파싱 → DB 저장)
"""
import sys
from pathlib import Path
PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.append(str(PROJECT_ROOT)) 

from csv_reader import read_and_parse_csv
from db_writer import recreate_table, save_to_db
from utils.path_manager import SCRAPYARD_CSV  

def main():
    # 1️⃣ 테이블 재생성
    recreate_table()

    # 2️⃣ CSV 읽기 + 주소 파싱
    df = read_and_parse_csv(SCRAPYARD_CSV)
    print(f"📦 {len(df)}개 레코드 파싱 완료\n")

    # 3️⃣ DB에 새로 저장
    save_to_db(df)

if __name__ == "__main__":
    main()