create user 'skn21-1'@'localhost' identified by '1111';

create user 'skn21-1'@'%' identified by '1111';

grant all privileges on *.* to 'skn21-1'@'localhost';

grant all privileges on *.* to 'skn21-1'@'%';

-- user 권한 조회
show grants for 'skn21-1'@'%';
show grants for 'skn21-1'@'localhost';

create database skn21 DEFAULT CHARACTER SET utf8mb4;

use skn21;


-- 지역 코드 마스터 테이블
CREATE TABLE REGION_CODES (
    CODE VARCHAR(2) NOT NULL PRIMARY KEY COMMENT '지역 코드 (PK, 01, 02, 11)',
    CODE_NAME VARCHAR(20) NOT NULL COMMENT '지역 명칭 (예: 서울특별시, 경기도)',
    CITY_NAME VARCHAR(50) COMMENT '대표 도시 명칭 (예: 서울, 경기, 인천)'
) DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

-- 지역 코드
INSERT INTO REGION_CODES (CODE, CODE_NAME, REPRESENTATIVE_CITY) VALUES
('02', '서울특별시', '서울'), -- 서울: 02
('01', '경기도', '경기'),     -- 경기: 01 (수정)
('11', '인천광역시', '인천');  -- 인천: 11 (수정)

-- 폐차장 정보 통합 테이블
CREATE TABLE SCRAPYARD_INFO (
    SY_ID BIGINT NOT NULL AUTO_INCREMENT PRIMARY KEY COMMENT '폐차장 고유 ID (PK)',
    SY_NAME VARCHAR(100) NOT NULL COMMENT '폐차장 명칭',
    CEO_NAME VARCHAR(50) COMMENT '대표자 명칭',
    CONTACT_NUMBER VARCHAR(20) COMMENT '대표 전화번호',
    ADDRESS VARCHAR(255) NOT NULL COMMENT '주소',
    REGION_CODE VARCHAR(2) NOT NULL COMMENT '광역 지역 코드 (FK: REGION_CODES.CODE)',
    SUBREGION_NAME VARCHAR(50) NOT NULL COMMENT '시/군/구 명칭',
    CREATED_AT DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT '데이터 최초 생성 일시',
    
    -- 외래 키 정의 (REGION_CODES 테이블과 조인)
    FOREIGN KEY (REGION_CODE) REFERENCES REGION_CODES(CODE)
) DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

