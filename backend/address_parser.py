"""
Author      : 신지용
Date        : 2025-10-22
Last Update : 2025-10-23
Description : 주소 문자열에서 광역시·도 및 시·군·구를 자동 추출
File Role   : 문자열 전처리 및 지역 단위 파싱 로직 담당
"""

import re

REGION_MAP = {
    "서울": "서울특별시",
    "서울시": "서울특별시",
    "서울특별시": "서울특별시",
    "경기": "경기도",
    "경기도": "경기도",
    "인천": "인천광역시",
    "인천시": "인천광역시",
    "인천광역시": "인천광역시",
}

def normalize_region(address: str):
    """광역시·도 단위 인식 (줄임말 포함)"""
    if not isinstance(address, str):
        return None
    for key, val in REGION_MAP.items():
        if address.startswith(key):  # 맨 앞에 등장하는 경우 우선
            return val
        if re.search(rf"\b{re.escape(key)}\b", address):
            return val
    return None


def extract_subregion(address: str, region_name: str | None):
    """
    단순 규칙:
      - '서울', '인천', '경기' 중 하나가 맨 앞에 있으면
        바로 뒤 토큰 중 '시', '군', '구'로 끝나는 단어 반환
    """
    if not isinstance(address, str):
        return None

    tokens = re.split(r"\s+", address.strip())
    if not tokens:
        return None

    # 1️⃣ 맨 앞 단어 확인
    first = tokens[0]
    if any(first.startswith(x) for x in ["서울", "인천", "경기"]):
        # 2️⃣ 바로 뒤 토큰 중 시·군·구 찾기
        for token in tokens[1:]:
            if token.endswith(("시", "군", "구")):
                return token
        return None

    # 3️⃣ 그 외의 경우: 일반 규칙 적용
    for token in tokens:
        if token.endswith(("구", "군", "시")):
            return token
    return None


def parse_address(address: str):
    region_name = normalize_region(address)
    subregion_name = extract_subregion(address, region_name)
    return region_name, subregion_name
