"""
Author      : 신지용 
Date        : 2025-10-23
Description : FAQ CSV 파일을 읽어서 DataFrame 생성
File Role   : CSV → pandas 변환 전용 (DB 저장 전 단계)
"""

import pandas as pd

def read_faq_csv():
    """
    FAQ CSV 파일을 읽어서 DataFrame으로 반환
    - 파일 경로: C:\\project\\project\\jiyong\\faq.csv
    - 필수 컬럼: QUESTION, ANSWER
    """
    csv_path = r"C:\project\project\jiyong\FAQ.csv"

    try:
        df = pd.read_csv(csv_path, encoding="utf-8")
        df.columns = [col.strip().upper() for col in df.columns]

        required_cols = {"QUESTION", "ANSWER"}
        missing = required_cols - set(df.columns)
        if missing:
            raise ValueError(f"❌ CSV에 필수 컬럼 누락됨: {missing}")

        print(f"📄 CSV에서 {len(df)}개의 FAQ 로드 완료")
        return df

    except FileNotFoundError:
        print(f"⚠️ 파일을 찾을 수 없습니다: {csv_path}")
        return pd.DataFrame(columns=["QUESTION", "ANSWER"])

    except Exception as e:
        print(f"⚠️ CSV 읽기 중 오류 발생: {e}")
        return pd.DataFrame(columns=["QUESTION", "ANSWER"])
