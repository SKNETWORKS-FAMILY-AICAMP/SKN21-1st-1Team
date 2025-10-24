# excel_to_json_converter_auto_fixed.py
import json, re
from typing import List, Dict

def _to_int(s: str) -> int:
    try:
        return int(s.replace(",", ""))
    except:
        return 0

def _numbers_from_line(line: str) -> List[int]:
    # 콤마 포함 숫자만 추출
    return [_to_int(x) for x in re.findall(r"[\d,]+", line)]

def _extract_region(line: str) -> str | None:
    """
    행 맨 앞의 한글 덩어리를 지역명으로 추출.
    '부     산', '대   구' 같은 경우도 전부 '부산', '대구'로 정규화.
    """
    # 맨 앞 한글(공백 포함) + 그 다음에 숫자가 시작되는 패턴을 찾는다
    m = re.match(r'^\s*([가-힣\s]+?)\s+[\d,]', line)
    if not m:
        # 숫자가 바로 안나와도, 한글만으로 이뤄진 첫 덩어리를 시도
        m2 = re.match(r'^\s*([가-힣\s]+)', line)
        if not m2:
            return None
        raw = m2.group(1)
    else:
        raw = m.group(1)
    # 한글만 남기고(공백/특수문자 제거) 지역명으로 사용
    name = re.sub(r'[^가-힣]', '', raw)
    return name if len(name) >= 2 else None

def _detect_vehicle_layout(nums_count: int) -> List[str] | None:
    """
    숫자 개수로 레이아웃 감지:
    - 31개: 승용/승합/화물/특수/기타 + 지역합계
    - 25개: 승용/승합/화물/특수 + 지역합계
    """
    if nums_count >= 31:
        return ["승용", "승합", "화물", "특수", "기타"]
    if nums_count >= 25:
        return ["승용", "승합", "화물", "특수"]
    return None

def convert_excel_text_to_json(text: str) -> List[Dict]:
    # 줄 전처리 (윈도/맥/리눅스 개행 섞여도 OK)
    lines = [l.strip() for l in text.replace("\r", "").split("\n") if l.strip()]

    # '지역' 헤더 라인을 느슨하게 탐지 (공백/탭/특수공백 포함해도 OK)
    start = 0
    for i, l in enumerate(lines):
        if "지역" in l:
            start = i + 1
            break

    results: List[Dict] = []

    for l in lines[start:]:
        # '합'으로 시작(예: '합     계', '합계')하는 총계 행은 무시
        if re.match(r'^\s*합', l):
            continue

        region = _extract_region(l)
        if not region:
            # 지역명 못 찾으면 스킵
            continue

        nums = _numbers_from_line(l)
        if not nums:
            continue

        vehicles = _detect_vehicle_layout(len(nums))
        if not vehicles:
            # 디버그: 이상치 라인
            # print(f"⚠️ {region} 행: 숫자 {len(nums)}개(예상 25~31) → 건너뜀")
            continue

        # 전체 숫자 배열을 31 길이에 맞춰 보정 (부족: 0 패딩, 초과: 절단)
        # 31 = (차종수 최대 5) * (용도 2) * (필드 3) + (지역합계 1)
        if len(nums) < 31:
            nums = nums + [0] * (31 - len(nums))
        elif len(nums) > 31:
            nums = nums[:31]

        idx = 0
        obj: Dict = {"지역": region}

        for v in vehicles:
            obj[v] = {}
            for u in ["사업용", "비사업용"]:
                ja, ta, sm = nums[idx:idx+3]
                idx += 3
                obj[v][u] = {"자도": ja, "타도": ta, "합계": sm}

        # 마지막 값은 지역 합계로 사용
        obj["합계"] = nums[-1]
        results.append(obj)

    return results


if __name__ == "__main__":
    # 같은 폴더의 input.txt 읽기 (CP949/UTF-8 모두 시도)
    try:
        with open("input.txt", "r", encoding="utf-8") as f:
            raw = f.read()
    except UnicodeDecodeError:
        with open("input.txt", "r", encoding="cp949") as f:
            raw = f.read()

    data = convert_excel_text_to_json(raw)

    with open("output.json", "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    print(f"✅ 변환 완료: {len(data)}개 지역 → output.json")
