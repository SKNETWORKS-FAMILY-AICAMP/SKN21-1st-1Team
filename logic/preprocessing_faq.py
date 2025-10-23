"""
Author: 최주원
Date: 2025-10-23
Description: 폐차장 faq Data 선처리 프로그램
"""
from flask import Flask, jsonify, Response
import mysql.connector
import csv
import codecs
import json

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False

# MySQL 연결 설정 함수
def get_db_connection():
    try:
        mydb = mysql.connector.connect(  # 얘네는 MYSQL 사용자 정보이기에 바꾸셔야해요
            host="127.0.0.1",
            port=3306,
            user="joshua",  
            password="1111",
            database="faq_db",  
            charset='utf8mb4'
        )
        print("MySQL 연결 성공")
        return mydb
    except Exception as e:
        print(f"MySQL 연결 오류: {e}")
        return None

# CSV 파일에서 데이터를 읽어 MySQL 데이터베이스에 삽입하는 함수
def load_data_from_csv_to_mysql():
    file_path = 'C:/Users/juwon/OneDrive/Desktop/sk1/SKN21-1st-1Team/FAQ.csv' # FAQ.CSV 파일 경로
    mydb = None
    mycursor = None
    try:
        mydb = get_db_connection()
        if mydb is None:
            print("오류: MySQL 연결 실패")
            return False

        mycursor = mydb.cursor()
        print("MySQL 커서 생성 성공")

        # 테이블 삭제 (테이블이 존재하는 경우)
        try:
            mycursor.execute("DROP TABLE IF EXISTS faqs")
            print("기존 테이블 삭제 성공")
        except Exception as e:
            print(f"테이블 삭제 오류: {e}")
            return False

        # 테이블 생성 (컬럼 정의 및 AUTO_INCREMENT 설정 포함)
        try:
            mycursor.execute("""
                CREATE TABLE faqs (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    question TEXT,
                    answer TEXT
                )
            """)
            print("테이블 생성 성공")
        except Exception as e:
            print(f"테이블 생성 오류: {e}")
            return False

        with codecs.open(file_path, 'r', encoding='utf-8-sig') as csvfile:
            reader = csv.reader(csvfile)
            header = next(reader)  # 헤더 추출
            print(f"CSV 헤더: {header}")

            for row in reader:
                faq = {}
                for i, col in enumerate(header):
                    faq[col] = row[i].strip()  # 각 필드를 디코딩
                print(f"CSV 행 데이터: {faq}")

                # MySQL에 데이터 삽입 (id 컬럼 제외)
                sql = "INSERT INTO faqs (question, answer) VALUES (%s, %s)"
                val = (faq['question'], faq['answer'])
                try:
                    mycursor.execute(sql, val)
                    print("데이터 삽입 성공")
                except Exception as e:
                    print(f"데이터 삽입 오류: {e}")
                    mydb.rollback()
                    return False

        mydb.commit()  # 변경 사항 저장
        print("CSV 파일 데이터를 MySQL로 성공적으로 로드했습니다.")
        return True  # 성공적으로 데이터를 삽입했음을 반환

    except FileNotFoundError:
        print("오류: CSV 파일을 찾을 수 없습니다.")
        return False
    except Exception as e:
        if mydb:
            mydb.rollback()  # 오류 발생 시 롤백
        print(f"오류 발생: {e}, 타입: {type(e)}")  # 오류 메시지 및 타입 출력
        return False
    finally:
        if mycursor:
            mycursor.close()
        if mydb:
            mydb.close()

@app.route('/', methods=['GET'])
def get_faqs():
    # CSV 파일 데이터를 MySQL로 로드 (매번 실행)
    if load_data_from_csv_to_mysql():
        print("CSV 파일 데이터를 MySQL로 성공적으로 로드했습니다.")
    else:
        return jsonify({'error': 'CSV 파일 데이터를 MySQL로 로드하는 데 실패했습니다.'}), 500

    try:
        mydb = get_db_connection()
        mycursor = mydb.cursor(dictionary=True)
        mycursor.execute("SELECT id, question, answer FROM faqs")
        faqs = mycursor.fetchall()

        # JSON 응답 생성
        json_data = json.dumps(faqs, ensure_ascii=False)
        return Response(json_data, mimetype='application/json')

    except Exception as e:
        print(f"DB 오류 발생: {e}")
        return jsonify({'error': str(e)}), 500
    finally:
        if 'mycursor' in locals() and mycursor:
            mycursor.close()
        if 'mydb' in locals() and mydb:
            mydb.close()

if __name__ == '__main__':
    app.run(debug=True, use_reloader=False)
