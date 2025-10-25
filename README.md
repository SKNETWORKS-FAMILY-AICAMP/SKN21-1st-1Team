# 폐차 정보 조회 플랫폼 차 버릴래

<img src="image/logo.png" alt="프로젝트 로고" width="auto">

폐차장 조회 및 정보 플랫폼.

## 📋 프로젝트 개요
**차 버릴래**는 수도권 지역의 폐차장 위치를 확인하고, 절차, 통계를 확인할 수 있는 플랫폼입니다.

## 🎯 필요성
- 공공데이터와 크롤링 데이터를 기반으로 폐차에 필요한 절차와 통계, 위치파악 가능.
- 필요한 통계 데이터를 다운로드 가능.

## 👥 팀 구성 및 역할 분담

**Team 차 버릴래**
<table>
<tr>
<td align="center" width="200" style="vertical-align: top; height: 300px;">
  <img src="image/park.png" width="150" height="150" style="border-radius: 50%; object-fit: cover;" alt="박수빈"/>
  <br />
  <h3 style="margin: 10px 0 5px 0;">박수빈</h3>
  <p style="margin: 5px 0;">역할 | PM</p>
  <div style="margin-top: 10px;">
    <a href="https://github.com/sbpark2930-ui">
      <img src="https://img.shields.io/badge/GitHub-181717?style=flat-square&logo=GitHub&logoColor=white"/>
    </a>
  </div>
</td>

<td align="center" width="200" style="vertical-align: top; height: 300px;">
<img src="image/sin.png" width="150" height="150" style="border-radius: 50%; object-fit: cover;" alt="신지용"/>
  <br />
<br />
<h3 style="margin: 10px 0 5px 0;">신지용</h3>
<p style="margin: 5px 0;">역할 | BACK</p>
<div style="margin-top: 10px;">
<a href="https://github.com/sjy361872">
<img src="https://img.shields.io/badge/GitHub-181717?style=flat-square&logo=GitHub&logoColor=white"/>
</a>
</div>
</td>
<td align="center" width="200" style="vertical-align: top; height: 300px;">
<img src="image/choi.jpg" width="150" height="150" style="border-radius: 50%; object-fit: cover;" alt="최자슈아주원"/>
  <br />
<br />
<h3 style="margin: 10px 0 5px 0;">최자슈아주원</h3>
<p style="margin: 5px 0;">역할 | BACK</p>
<div style="margin-top: 10px;">
<a href="https://github.com/reasonableplan">
<img src="https://img.shields.io/badge/GitHub-181717?style=flat-square&logo=GitHub&logoColor=white"/>
</a>
</div>
</td>
<td align="center" width="200" style="vertical-align: top; height: 300px;">
<img src="image/lee.png" width="150" height="150" style="border-radius: 50%; object-fit: cover;" alt="이의정"/>
<br />
<h3 style="margin: 10px 0 5px 0;">이의정</h3>
<p style="margin: 5px 0;">역할 | 크롤링</p>
<div style="margin-top: 10px;">
<a href="https://github.com/lee910814">
<img src="https://img.shields.io/badge/GitHub-181717?style=flat-square&logo=GitHub&logoColor=white"/>
</a>
</div>
</td>
<td align="center" width="200" style="vertical-align: top; height: 300px;">
<img src="image/jang.png" width="150" height="150" style="border-radius: 50%; object-fit: cover;" alt="장이선"/>
<br />
<h3 style="margin: 10px 0 5px 0;">장이선</h3>
<p style="margin: 5px 0;">역할 | DB/FRONT</p>
<div style="margin-top: 10px;">
<a href="https://github.com/jang-yiseon">
<img src="https://img.shields.io/badge/GitHub-181717?style=flat-square&logo=GitHub&logoColor=white"/>
</a>
</div>
<td align="center" width="200" style="vertical-align: top; height: 300px;">
<img src="image/moon.jpg" width="150" height="150" style="border-radius: 50%; object-fit: cover;" alt="문지영"/>
<br />
<h3 style="margin: 10px 0 5px 0;">문지영</h3>
<p style="margin: 5px 0;">역할 | FRONT</p>
<div style="margin-top: 10px;">
<a href="https://github.com/moon-613">
<img src="https://img.shields.io/badge/GitHub-181717?style=flat-square&logo=GitHub&logoColor=white"/>
</a>
</div>
</td>
</tr>
</table>

## 기술 스택

### Frontend
![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=Streamlit&logoColor=white)
![HTML](https://img.shields.io/badge/HTML5-E34F26?style=for-the-badge&logo=html5&logoColor=white)
![CSS](https://img.shields.io/badge/CSS3-1572B6?style=for-the-badge&logo=css3&logoColor=white)

### Backend & Database
![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![MySQL](https://img.shields.io/badge/MySQL-4479A1?style=for-the-badge&logo=mysql&logoColor=white)
![Flask](https://img.shields.io/badge/Flask-000000?style=for-the-badge&logo=flask&logoColor=white)
![JSON](https://img.shields.io/badge/JSON-000000?style=for-the-badge&logo=json&logoColor=white)

### Data Processing & Analysis
![Pandas](https://img.shields.io/badge/Pandas-150458?style=for-the-badge&logo=pandas&logoColor=white)
![Matplotlib](https://img.shields.io/badge/Matplotlib-11557c?style=for-the-badge)

### Web Scraping
![Selenium](https://img.shields.io/badge/Selenium-43B02A?style=for-the-badge&logo=selenium&logoColor=white)

## 프로젝트 구조
<img src="image/flow.png" alt="flow" width="auto">

본 프로젝트는 데이터 사전 처리 단계와 실시간 조회 서비스 단계로 구성됩니다.

1. 데이터 사전 처리 (Pre-processing)
애플리케이션 서버가 실행되기 전, 사용자에게 제공할 데이터를 미리 준비하는 단계입니다.

데이터 수집: Python을 이용해 필요한 원본 데이터를 크롤링합니다.

데이터 저장 (1차): 수집된 데이터를 CSV 파일 형태로 로컬에 저장합니다.

데이터베이스 적재 (Pre-load): 저장된 CSV 파일을 가공하여 메인 데이터베이스MySQL에 삽입(Insert)합니다. 이 과정을 통해 서버는 항상 정제된 최신 데이터를 기준으로 실행을 시작합니다.

2. 실시간 조회 서비스 (Runtime Flow)
사용자가 시스템을 이용하는 실제 동작 흐름입니다. 프론트엔드(Streamlit)와 백엔드(Flask)가 명확히 분리되어 동작합니다.

① 사용자 인증: 사용자는 Streamlit(프론트엔드) 화면을 통해 시스템에 로그인합니다.

② 데이터 요청 (Front → Back): 사용자가 특정 데이터를 조회하면, Streamlit은 조회에 필요한 파라미터(검색어, 조건 등)를 JSON 형식으로 구성하여 Flask(백엔드) API 서버에 전송(Request)합니다.

③ 백엔드 처리 (Back-end Logic):

Flask 서버는 수신한 JSON 데이터를 파싱(Parsing)합니다.

파싱된 파라미터를 기반으로 적절한 SQL 쿼리문을 생성합니다.

생성된 SQL을 데이터베이스(DB)로 전송하여 실시간으로 데이터를 조회합니다.

④ 데이터 응답 (Back → Front):

DB로부터 조회된 결과값을 다시 JSON 형식으로 가공합니다.

이 JSON 데이터를 Streamlit(프론트엔드) 측에 응답(Response)으로 전송합니다.

⑤ 결과 표시: Streamlit은 백엔드로부터 받은 JSON 데이터를 이용해 사용자 화면에 조회 결과를 동적으로 표시합니다.

## 데이터베이스 구조
<img src="image/erd.png" alt="ERD" width="auto">

## 주요 기능

## 1. 🏠 메인 도메인 화면 (문지영)
- 홈화면 및 메뉴 구현.
- 사용자 친화적인 UI 사용.

<img src="image/main.gif" alt="main" width="auto">

## 2. 🔍 폐차장 검색 / 🔐 로그인 시스템 (신지용)
- DB에 있는 user정보를 통해 로그인 시스템 구현.
- 수도권 폐차장 검색.
- 크롤링 된 Data를 기반으로 상세 정보 제공.

<img src="image/login.gif" alt="login" width="auto">

<img src="image/search.gif" alt="search" width="auto">

## 3. 📍 지도 위치 시스템 (장이선)
- 조회 된 폐차장을 카카오맵에 구현.

## 4. 📰 카드 뉴스 (이의정)
- 폐차와 관련된, 다양한 언론사의 뉴스정보를 제공.

<img src="image/news.gif" alt="news" width="auto">

## 5. 📊 실적 데이터 (박수빈)
- 최근 약 10년간의 조건에 따른 전국 폐차 정보 제공.
- 필요한 데이터 액셀 형태로 다운로드 제공.
- 시각화 된, 차트 및 표 제공.

<img src="image/dataTable.gif" alt="news" width="auto">

## 6. ❓ FAQ (Joshua Juwon Choi)
- 폐차와 관련하여 자주 묻는 질문 List 를 출력.
- 클릭 시, 답변 제공.

<img src="image/faq.gif" alt="news" width="auto">

## 📚 자료 출처
한국자동차해체재활용협동조합(KADCO, Korea Automobile Recycling cooperative) 
https://www.kadra.or.kr/kadra/contents/main/main.html

## 📈 기대효과

### 사용자
- 수도권 이용자들의 폐차를 위한 위치 확인 가능.
- 폐차 이전, 필요한 정보를 제공하여 선택지를 지원.
- 통계 정보를 통한, 수도권 폐차 정보 확인에 용이.

### 학습/팀 성과
- 공공데이터 + 크롤링 + DB + 시각화 프로젝트 경험
- Python, MySQL, Streamlit, Web Crawling 등 학습 내용을 종합 적용
- Flask 기반의 백엔드 API 서버를 구축, 사용자 요청에 따라 DB와 실시간으로 연동하여 최신화된 데이터를 JSON 형태로 제공하도록 구현.
- GitHub 협업과 DB 실습을 통한 실무 능력 강화

## 추가 구현하고 싶은 기능
- 폐차 보조금에 대한 업체를 광고 할 수 있는 게시판
- 로그인 한 유저를 관리할 수 있는 AdminPage 및 Adming 권한 Table
- 일정시간 페이지 비이동 시, TimeOut 기능
- 

### 아쉬운 점
- 폐차장과 관련 된 Data들의 크롤링이 쉽지 않아, 통계의 경우 엑셀파일을 Convert 하는 모듈을 작업하여 사용한 것.
- 시간의 부재로 flask API를 사용한 DB의 연동이 불안정한 사항.

## 회고
- 박수빈 상대적으로 프로그래밍 보단 설계 및 도움을 줄 수 있는 PM역할을 맡아 좋은 경험을 한거 같아 좋습니다.
    같이 열심히 해주신 팀원분들에게 감사인사 올립니다.

-

-

-

-

-
