from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import time
import os

# ✅ 크롬 옵션 설정
chrome_options = Options()
# chrome_options.add_argument("--headless")  # 백그라운드 실행 시 주석 해제
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")

# ✅ 드라이버 실행
driver = webdriver.Chrome(options=chrome_options)

# ✅ 크롤링할 지역 코드 리스트
region_codes = ['01', '02', '11']  # 01:경기, 02:서울, 11:인천
region_names = {'01':'경기', '02':'서울', '11':'인천'}

all_data = []

# ✅ 각 지역별 크롤링
for code in region_codes:
    url = f"https://www.kadra.or.kr/kadra/contents/sub01/01_01.html?srhCate={code}"
    driver.get(url)
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "table tbody tr"))
    )

    page = 1
    while True:
        print(f"{region_names[code]} 페이지 {page} 수집 중...")
        rows = driver.find_elements(By.CSS_SELECTOR, "table tbody tr")
        for row in rows:
            cols = [td.text.strip() for td in row.find_elements(By.TAG_NAME, "td")]
            if len(cols) >= 4:
                all_data.append({
                    "폐차장명": cols[0],
                    "대표자명": cols[1],
                    "주소": cols[2],
                    "전화번호": cols[3],
                    # 지역 컬럼은 CSV에 안 쓰기 위해 내부용으로만 기록
                    "지역": region_names[code]
                })
        # 다음 페이지
        try:
            next_button = driver.find_element(By.LINK_TEXT, str(page + 1))
            next_button.click()
            page += 1
            time.sleep(2)
        except:
            print(f"{region_names[code]} 모든 페이지 수집 완료 ✅")
            break

driver.quit()

# ✅ DataFrame으로 변환
df = pd.DataFrame(all_data)

# ✅ 지역 순서대로 정렬 (서울 → 인천 → 경기)
region_order = ['서울','인천','경기']
df_sorted = pd.concat([df[df['지역']==region] for region in region_order], ignore_index=True)

# ✅ 지역 컬럼 제거 (CSV에는 안 나오게)
df_sorted = df_sorted.drop(columns=['지역'], errors='ignore')

# ✅ 최종 CSV 저장
df_sorted.to_csv("폐차장_전체.csv", index=False, encoding='utf-8-sig')
print("✅ 폐차장_전체.csv 저장 완료!")
