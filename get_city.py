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

# ✅ 폐차장 정보 페이지
url = "https://www.kadra.or.kr/kadra/contents/sub01/01_01.html?srhCate=02" 

driver.get(url)

# ✅ 테이블 로드 기다리기
WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.CSS_SELECTOR, "table tbody tr"))
)

data = []

# ✅ 첫 페이지부터 반복
page = 1
while True:
    print(f"페이지 {page} 수집 중...")
    rows = driver.find_elements(By.CSS_SELECTOR, "table tbody tr")

    # 각 행에서 td 텍스트 추출
    for row in rows:
        cols = [td.text.strip() for td in row.find_elements(By.TAG_NAME, "td")]
        # 테이블 형식 맞춰서 필요한 부분만 추출
        if len(cols) >= 4:
            data.append({
                "폐차장명": cols[0],
                "대표자명": cols[1],
                "주소": cols[2],
                "전화번호": cols[3],
            })

    # 다음 페이지 버튼 찾기
    try:
        next_button = driver.find_element(By.LINK_TEXT, str(page + 1))
        next_button.click()
        page += 1
        time.sleep(2)
    except:
        print("모든 페이지 수집 완료 ✅")
        break

# ✅ DataFrame으로 변환
df = pd.DataFrame(data)



driver.quit()

print(f"총 {len(df)}개 폐차장 정보 저장 완료 ✅")
print(df.head())


# #csv저장 
# df.to_csv("폐차장목록.csv", index=False,encoding="UTF-8")

# ✅ 주소를 기반으로 지역 구분
def get_region(address):
    if '서울' in address:
        return '서울'
    elif '경기' in address:
        return '경기'
    elif '인천' in address:
        return '인천'
    else:
        return '기타'

df['지역'] = df['주소'].apply(get_region)

# ✅ 지역별로 CSV 저장 (기존 데이터와 합쳐서 저장)
for region in ['서울', '경기', '인천']:
    region_df = df[df['지역'] == region]
    if not region_df.empty:
        filename = f"{region}.csv"
        if os.path.exists(filename):
            old_df = pd.read_csv(filename)
            new_df = pd.concat([old_df, region_df], ignore_index=True)
            new_df.to_csv(filename, index=False, encoding='utf-8-sig')
            print(f"✅ {region}.csv 에 데이터 추가 저장 완료!")
        else:
            region_df.to_csv(filename, index=False, encoding='utf-8-sig')
            print(f"✅ {region}.csv 새로 생성 완료!")