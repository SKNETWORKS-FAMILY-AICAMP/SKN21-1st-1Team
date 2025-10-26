from pathlib import Path

# 프로젝트 최상위 경로 설정
BASE_DIR = Path(__file__).resolve().parent.parent

# 'data_csv' 폴더를 가리키는지 확인!
DATA_DIR = BASE_DIR / "data_csv" 

FAQ_DIR = DATA_DIR / "faq"
SCRAPYARD_DIR = DATA_DIR / "scrapyard"
NEWS_DIR = DATA_DIR / "news"

FAQ_CSV = FAQ_DIR / "faq.csv"
SCRAPYARD_CSV = SCRAPYARD_DIR / "scrapyard.csv"
NEWS_CSV = NEWS_DIR / "google_news_limited.csv"

print(NEWS_CSV)