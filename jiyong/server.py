"""
Author      : 신지용 
Date        : 2025-10-22
Last Update : 2025-10-23
Description : Flask 기반 폐차장 데이터 조회 API 서버
File Role   : DB 데이터를 JSON 형태로 반환하는 백엔드 서버
"""

from flask import Flask, Response, request
import pymysql, json
from db_config import DB_CONFIG

app = Flask(__name__)

def get_connection():
    return pymysql.connect(**DB_CONFIG)

@app.route("/")
def home():
    # 메인 화면
    return """
    <h2>🚗 수도권 폐차장 API 서버</h2>
    <p>서버가 정상적으로 실행 중입니다 ✅</p>
    <p>사용 가능한 엔드포인트:</p>
    <ul>
        <li><b>/scrapyards</b> — 전체 폐차장 데이터 조회</li>
        <li><b>/scrapyards?region=서울특별시</b> — 지역별 조회</li>
        <li><b>/scrapyards?subregion=금천구</b> — 시군구별 조회</li>
    </ul>
    """
@app.route("/scrapyards", methods=["GET"])
def get_scrapyards():
    region_code = request.args.get("region")       # 예: 02
    subregion_code = request.args.get("subregion") # 예: 11680 등

    conn = get_connection()
    cursor = conn.cursor(pymysql.cursors.DictCursor)

    base_sql = """
        SELECT SY_ID, SY_NAME, CEO_NAME, CONTACT_NUMBER, ADDRESS,
               REGION_CODE, SUBREGION_NAME
        FROM SCRAPYARD_INFO
    """
    filters = []
    params = []

    if region_code:
        filters.append("REGION_CODE = %s")
        params.append(region_code)
    if subregion_code:
        filters.append("SUBREGION_CODE = %s")
        params.append(subregion_code)

    if filters:
        base_sql += " WHERE " + " AND ".join(filters)

    cursor.execute(base_sql, params)
    results = cursor.fetchall()
    conn.close()

    json_data = json.dumps(results, ensure_ascii=False)
    return Response(json_data, content_type="application/json; charset=utf-8")


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)
