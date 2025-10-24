"""
Author      : 신지용 
Date        : 2025-10-22
Last Update : 2025-10-23
Description : Flask 기반 폐차장 + FAQ 데이터 조회 API 서버
File Role   : DB 데이터를 JSON 형태로 반환하는 백엔드 서버
"""

from flask import Flask, Response, request, jsonify  
import pymysql, json                           
from db_config import DB_CONFIG

app = Flask(__name__)

def get_connection():
    return pymysql.connect(**DB_CONFIG, autocommit=True)


@app.route("/")
def home():
    # 메인 화면
    return """
    <!DOCTYPE html>
    <html lang="ko">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>API 서버 메인</title>
        <style>
            /* 깔끔한 모던 웹폰트 */
            body { 
                font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, 'Open Sans', 'Helvetica Neue', sans-serif; 
                margin: 0; 
                padding: 0; 
                display: flex; 
                justify-content: center; /* 중앙 정렬 */
                align-items: center; 
                min-height: 90vh; /* 화면 높이만큼 */
                background-color: #f4f7f6; /* 부드러운 배경색 */
            }
            /* 카드 형태의 메인 컨텐츠 영역 */
            .container { 
                max-width: 700px; 
                margin: 20px; 
                padding: 30px; 
                background-color: #ffffff; 
                border-radius: 10px; /* 둥근 모서리 */
                box-shadow: 0 4px 12px rgba(0,0,0,0.05); /* 은은한 그림자 */
                border: 1px solid #e0e0e0;
            }
            /* 프로젝트 타이틀 (Streamlit 버튼과 통일감 있는 파란색) */
            h1 { 
                color: #1158e0; 
                border-bottom: 2px solid #eee; 
                padding-bottom: 10px;
                display: flex;
                align-items: center;
            }
            h1 span {
                margin-left: 10px;
            }
            p { 
                font-size: 1.1rem; 
                color: #333; 
                line-height: 1.6; 
            }
            /* 서버 상태 배지 */
            .status { 
                display: inline-block;
                background-color: #e6f7ec; /* 초록색 배경 */
                color: #006421; /* 진한 초록색 글씨 */
                padding: 8px 15px; 
                border-radius: 20px; /* 캡슐 형태 */
                font-weight: bold; 
                font-size: 0.9rem;
            }
            h2 { 
                color: #333; 
                margin-top: 30px; 
                border-bottom: 1px solid #eee;
                padding-bottom: 5px;
            }
            /* API 엔드포인트 목록 */
            ul { 
                list-style-type: none; 
                padding-left: 0; 
            }
            li { 
                background-color: #f9f9f9; /* 목록 배경색 */
                margin-bottom: 10px; 
                padding: 15px; 
                border-radius: 5px; 
                border: 1px solid #eee;
                font-size: 1rem;
            }
            /* 코드(엔드포인트) 강조 스타일 */
            code { 
                font-family: 'SFMono-Regular', Consolas, 'Liberation Mono', Menlo, Courier, monospace;
                background-color: #eef; /* 연한 보라색 배경 */
                color: #1a0dab;
                padding: 3px 6px; 
                border-radius: 4px; 
                font-size: 0.95rem;
            }
            li small {
                color: #555;
                font-style: italic;
                margin-left: 5px;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🚙<span>수도권 폐차장 조회 API 서버</span></h1>
            
            <p>
                <b>AI 부트캠프 1차 프로젝트 TeamName : 남자셋 여자셋 </b><br>
                Streamlit 프론트엔드에 데이터를 제공하기 위한 백엔드 API 서버입니다.
            </p>
            
            <p>
                <b>서버 상태:</b> <span class="status">정상 작동 중 ✅</span>
            </p>

            <h2>⚙️ 사용 가능한 API 엔드포인트</h2>
            <ul>
                <li>
                    <strong>폐차장 검색:</strong> 
                    <code> /scrapyards</code>
                    <br><small>(예: /scrapyards?region=02&subregion=강서구)</small>
                </li>
                <li>
                    <strong>세부 지역(시/군/구) 조회:</strong> 
                    <code> /subregions</code>
                    <br><small>(예: /subregions?region=02)</small>
                </li>
                <li>
                    <strong>FAQ 목록:</strong> 
                    <code> /faqs</code>
                </li>
            </ul>
        </div>
    </body>
    </html>
    """


# 🚗 폐차장 데이터 조회
# 🏠 [신규 추가] 세부 지역(시/군/구) 목록 조회 API
@app.route("/subregions", methods=["GET"])
def get_subregions():
    # Streamlit에서 보낸 'region' 파라미터 (e.g., "02")
    region_code = request.args.get("region") 

    if not region_code:
        app.logger.warning("region_code 파라미터가 없습니다.")
        return jsonify([]) # 파라미터가 없으면 빈 리스트 반환

    conn = get_connection()
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    
    # REGION_CODE에 해당하는 SUBREGION_NAME을 중복 없이(DISTINCT) 조회
    sql = """
        SELECT DISTINCT SUBREGION_NAME 
        FROM SCRAPYARD_INFO 
        WHERE REGION_CODE = %s
        ORDER BY SUBREGION_NAME
    """
    
    try:
        cursor.execute(sql, (region_code,))
        results = cursor.fetchall()
        
        # DB 결과는 [{'SUBREGION_NAME': '강남구'}, ...] 형태
        # 이 딕셔너리 리스트에서 값만 추출하여 ['강남구', ...] 리스트로 변환
        subregion_list = [item['SUBREGION_NAME'] for item in results if item['SUBREGION_NAME']]
        
        app.logger.debug(f"Region {region_code} subregions: {subregion_list}")
        
    except Exception as e:
        app.logger.error(f"Error fetching subregions: {e}")
        subregion_list = []
    finally:
        conn.close()

    # JSON 리스트로 반환 (한글이 깨지지 않도록 ensure_ascii=False 설정)
    return Response(json.dumps(subregion_list, ensure_ascii=False), content_type="application/json; charset=utf-8")

# 🚗 [추가!] 폐차장 데이터 조회 (이 부분이 빠져있었습니다!)
@app.route("/scrapyards", methods=["GET"])
def get_scrapyards():
    region_code = request.args.get("region")
    subregion_name = request.args.get("subregion")

    if region_code:
        region_code = region_code.strip()
    if subregion_name:
        subregion_name = subregion_name.strip()

    print("[DEBUG] region_code:", region_code, "subregion_name:", subregion_name)

    conn = get_connection()
    cursor = conn.cursor(pymysql.cursors.DictCursor)

    base_sql = """
        SELECT SY_ID, SY_NAME, CEO_NAME, CONTACT_NUMBER, ADDRESS,
               REGION_CODE, SUBREGION_NAME
        FROM SCRAPYARD_INFO
    """
    filters = []
    params = []

    # ✅ 정확히 일치 비교
    if region_code:
        filters.append("REGION_CODE = %s")
        params.append(region_code)

    # ✅ 부분 일치로 (금천 / 금천구 / 금천시 모두 검색)
    if subregion_name:
        filters.append("SUBREGION_NAME LIKE %s")
        params.append(f"%{subregion_name}%")

    if filters:
        base_sql += " WHERE " + " AND ".join(filters)

    print("[DEBUG SQL]", base_sql, params)

    cursor.execute(base_sql, params)
    results = cursor.fetchall()
    conn.close()

    return Response(json.dumps(results, ensure_ascii=False), content_type="application/json; charset=utf-8")


# 💬 FAQ 데이터 조회
@app.route("/faqs", methods=["GET"])
def get_faqs():
    conn = get_connection()
    cursor = conn.cursor(pymysql.cursors.DictCursor)

    query = """
        SELECT id AS FAQ_ID, question AS QUESTION, answer AS ANSWER
        FROM FAQ_INFO
        ORDER BY id ASC;
    """
    cursor.execute(query)
    results = cursor.fetchall()
    conn.close()

    json_data = json.dumps(results, ensure_ascii=False)
    return Response(json_data, content_type="application/json; charset=utf-8")


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)
