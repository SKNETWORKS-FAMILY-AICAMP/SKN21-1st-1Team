"""
Author      : 신지용 
Date        : 2025-10-22
Last Update : 2025-10-24 (회원관리 API 추가)
Description : Flask 기반 폐차장 + FAQ + 회원관리 데이터 조회 API 서버
File Role   : DB 데이터를 JSON 형태로 반환하는 백엔드 서버
"""

from flask import Flask, Response, request, jsonify  
import pymysql, json
# ❗️ [추가] 비밀번호 해시를 위한 라이브러리
from werkzeug.security import generate_password_hash, check_password_hash
from db_config import DB_CONFIG

app = Flask(__name__)

def get_connection():
    return pymysql.connect(**DB_CONFIG, autocommit=True)


@app.route("/")
def home():
    # 메인 화면 (기존과 동일)
    return """
    <!DOCTYPE html>
    <html lang="ko">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>API 서버 메인</title>
        <style>
            /* ... (기존 CSS 스타일 동일) ... */
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
            .container { 
                max-width: 700px; 
                margin: 20px; 
                padding: 30px; 
                background-color: #ffffff; 
                border-radius: 10px; /* 둥근 모서리 */
                box-shadow: 0 4px 12px rgba(0,0,0,0.05); /* 은은한 그림자 */
                border: 1px solid #e0e0e0;
            }
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
                <li>
                    <strong>로그인:</strong> 
                    <code> /login</code> (POST)
                </li>
                <li>
                    <strong>회원가입:</strong> 
                    <code> /register</code> (POST)
                </li>
            </ul>
        </div>
    </body>
    </html>
    """

# 🚗 폐차장 데이터 조회 (기존과 동일)
@app.route("/subregions", methods=["GET"])
def get_subregions():
    region_code = request.args.get("region") 
    if not region_code:
        app.logger.warning("region_code 파라미터가 없습니다.")
        return jsonify([]) 

    conn = get_connection()
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    sql = """
        SELECT DISTINCT SUBREGION_NAME 
        FROM SCRAPYARD_INFO 
        WHERE REGION_CODE = %s
        ORDER BY SUBREGION_NAME
    """
    
    try:
        cursor.execute(sql, (region_code,))
        results = cursor.fetchall()
        subregion_list = [item['SUBREGION_NAME'] for item in results if item['SUBREGION_NAME']]
        app.logger.debug(f"Region {region_code} subregions: {subregion_list}")
    except Exception as e:
        app.logger.error(f"Error fetching subregions: {e}")
        subregion_list = []
    finally:
        conn.close()

    return Response(json.dumps(subregion_list, ensure_ascii=False), content_type="application/json; charset=utf-8")

# 🚗 폐차장 데이터 조회 (기존과 동일)
@app.route("/scrapyards", methods=["GET"])
def get_scrapyards():
    region_code = request.args.get("region")
    subregion_name = request.args.get("subregion")

    if region_code:
        region_code = region_code.strip()
    if subregion_name:
        subregion_name = subregion_name.strip()

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
    if subregion_name:
        filters.append("SUBREGION_NAME LIKE %s")
        params.append(f"%{subregion_name}%")

    if filters:
        base_sql += " WHERE " + " AND ".join(filters)

    cursor.execute(base_sql, params)
    results = cursor.fetchall()
    conn.close()

    return Response(json.dumps(results, ensure_ascii=False), content_type="application/json; charset=utf-8")

# 💬 FAQ 데이터 조회 (기존과 동일)
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

# -----------------------------------------------------------------
# 👤 [신규] 회원 관리 API
# -----------------------------------------------------------------

# 👤 1. 회원가입 API
@app.route("/register", methods=["POST"])
def register_user():
    data = request.json
    username = data.get("username")
    password = data.get("password")

    if not username or not password:
        return jsonify({"success": False, "message": "아이디와 비밀번호를 모두 입력하세요."}), 400

    conn = get_connection()
    cursor = conn.cursor()
    try:
        # 아이디 중복 확인
        sql_check = "SELECT user_id FROM USER_INFO WHERE user_id = %s"
        cursor.execute(sql_check, (username,))
        if cursor.fetchone():
            return jsonify({"success": False, "message": "이미 존재하는 아이디입니다."}), 409

        # 비밀번호 해시
        hashed_pw = generate_password_hash(password)
        
        # 새 사용자 삽입
        sql_insert = "INSERT INTO USER_INFO (user_id, user_pw) VALUES (%s, %s)"
        cursor.execute(sql_insert, (username, hashed_pw))
        
        return jsonify({"success": True, "message": "회원가입이 완료되었습니다."}), 201

    except Exception as e:
        app.logger.error(f"Error during registration: {e}")
        return jsonify({"success": False, "message": "서버 오류가 발생했습니다."}), 500
    finally:
        conn.close()

# 👤 2. 로그인 API
@app.route("/login", methods=["POST"])
def login_user():
    data = request.json
    username = data.get("username")
    password = data.get("password")

    if not username or not password:
        return jsonify({"success": False, "message": "아이디와 비밀번호를 입력하세요."}), 400

    conn = get_connection()
    # ❗️ [수정] DictCursor로 변경 (컬럼명으로 접근하기 위해)
    cursor = conn.cursor(pymysql.cursors.DictCursor) 
    try:
        sql = "SELECT user_pw FROM USER_INFO WHERE user_id = %s"
        cursor.execute(sql, (username,))
        user_row = cursor.fetchone()

        if user_row and check_password_hash(user_row['user_pw'], password):
            # 로그인 성공
            return jsonify({"success": True, "message": "로그인 성공!"})
        else:
            # 사용자가 없거나 비밀번호 불일치
            return jsonify({"success": False, "message": "아이디 또는 비밀번호가 잘못되었습니다."}), 401

    except Exception as e:
        app.logger.error(f"Error during login: {e}")
        return jsonify({"success": False, "message": "서버 오류가 발생했습니다."}), 500
    finally:
        conn.close()

# 👤 3. 회원탈퇴 API
@app.route("/withdraw", methods=["POST"])
def withdraw_user():
    data = request.json
    username = data.get("username")
    password = data.get("password")

    if not username or not password:
        return jsonify({"success": False, "message": "아이디와 비밀번호를 입력하세요."}), 400

    conn = get_connection()
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    try:
        # 1. 먼저 사용자가 맞는지 (로그인과 동일하게) 확인
        sql_check = "SELECT user_pw FROM USER_INFO WHERE user_id = %s"
        cursor.execute(sql_check, (username,))
        user_row = cursor.fetchone()

        if user_row and check_password_hash(user_row['user_pw'], password):
            # 2. 사용자가 맞으면 삭제
            sql_delete = "DELETE FROM USER_INFO WHERE user_id = %s"
            cursor.execute(sql_delete, (username,))
            return jsonify({"success": True, "message": "회원탈퇴가 완료되었습니다."})
        else:
            # 비밀번호 불일치
            return jsonify({"success": False, "message": "비밀번호가 잘못되었습니다."}), 401

    except Exception as e:
        app.logger.error(f"Error during withdrawal: {e}")
        return jsonify({"success": False, "message": "서버 오류가 발생했습니다."}), 500
    finally:
        conn.close()


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)