"""
Author: 
Date: 2025-10-22
Description: 폐차장 faq Data 선처리 프로그램
"""

# 받은 Data를 Insert 혹은 Update 하기 위한 SQL문 작성 필요.
# import csv
# import pymysql

# # MySQL 연결 설정
# conn = pymysql.connect(
#     host='127.0.0.1',
#     port=3306,
#     user='root',
#     password='1234',
#     db='testdb',
#     charset='utf8mb4'
# )

# cursor = conn.cursor()

# # CSV 파일 경로
# file_path = r'C:\project\SKN21-1st-1Team\test\scrap_yard_data.csv'

# # CSV 읽어서 DB에 저장
# with open(file_path, mode='r', encoding='utf-8-sig') as file:
#     reader = csv.DictReader(file)
#     for row in reader:
#         업체명 = row.get('업체명', '').strip()
#         담당자 = row.get('담당자', '').strip()
#         주소 = row.get('주소', '').strip()
#         전화번호 = row.get('전화번호', '').strip()

#         sql = """
#             INSERT INTO scrap_yard (업체명, 담당자, 주소, 전화번호)
#             VALUES (%s, %s, %s, %s)
#         """
#         cursor.execute(sql, (업체명, 담당자, 주소, 전화번호))

# # 커밋 및 종료
# conn.commit()
# cursor.close()
# conn.close()

# print("✅ CSV 데이터가 MySQL DB에 성공적으로 저장되었습니다.")

# import json      # ✅ 이거 추가
# from flask import Flask
# import csv

# app = Flask(__name__)

# @app.route('/read-csv', methods=['GET'])
# def read_csv():
#     file_path = r'C:\project\SKN21-1st-1Team\test\scrap_yard_data.csv'
#     data_preview = []

#     with open(file_path, mode='r', encoding='utf-8-sig') as f:
#         reader = csv.DictReader(f)
#         for row in reader:
#             data_preview.append(row)

#     return app.response_class(
#         response=json.dumps({
#             "message": "✅ CSV 파일 읽기 성공",
#             "row_count": len(data_preview),
#             "preview": data_preview[:3]
#         }, ensure_ascii=False, indent=2),
#         mimetype='application/json'
#     )

# if __name__ == '__main__':
#     app.run(debug=True)

import json
from flask import Flask
import csv
import pymysql

app = Flask(__name__)

#  MySQL 연결 설정
def get_connection():
    return pymysql.connect(
        host='127.0.0.1',
        user='root',
        password='1234',  #  본인 비밀번호로 수정
        db='testdb',
        charset='utf8mb4',
        cursorclass=pymysql.cursors.DictCursor
    )

@app.route('/upload-db', methods=['GET'])
def upload_to_db():
    file_path = r'C:\project\SKN21-1st-1Team\test\scrap_yard_data.csv'
    data_preview = []

    #  1️⃣ CSV 읽기
    with open(file_path, mode='r', encoding='cp949') as f:
        reader = csv.DictReader(f)
        for row in reader:
            data_preview.append(row)

    #  2️⃣ DB 연결
    conn = get_connection()
    cur = conn.cursor()

    #  3️⃣ 테이블 생성 (없을 경우 자동 생성)
    create_table_sql = """
    CREATE TABLE IF NOT EXISTS SCRAPYARD_INFO (
        id INT AUTO_INCREMENT PRIMARY KEY,
        폐차장명 VARCHAR(100),
        대표자명 VARCHAR(50),
        주소 VARCHAR(255),
        전화번호 VARCHAR(30)
    ) CHARACTER SET utf8mb4;
    """
    cur.execute(create_table_sql)

    #  4️⃣ 데이터 삽입
    for row in data_preview:
        sql = """
        INSERT INTO SCRAPYARD_INFO (name, owner, address, phone)
        VALUES (%s, %s, %s, %s)
        """
        cur.execute(sql, (
            row.get('폐차장명'),
            row.get('대표자명'),
            row.get('주소'),
            row.get('전화번호')
        ))


    conn.commit()
    cur.close()
    conn.close()

    #  5️⃣ 응답 반환
    return app.response_class(
    response=json.dumps({
        "message": f"✅ DB 등록 완료 ({len(data_preview)}건)",
        "preview": data_preview[:3]
    }, ensure_ascii=False, indent=2).encode('utf-8'),
    mimetype='application/json; charset=utf-8'
)

@app.route('/scrapyards', methods=['GET'])
def get_scrapyards():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("SELECT * FROM SCRAPYARD_INFO ORDER BY id DESC;")
    rows = cur.fetchall()

    cur.close()
    conn.close()

    # 한글 깨짐 방지
    return app.response_class(
        response=json.dumps({
            "count": len(rows),
            "data": rows
        }, ensure_ascii=False, indent=2),
        mimetype='application/json'
    )

if __name__ == '__main__':
    app.run(debug=True)
