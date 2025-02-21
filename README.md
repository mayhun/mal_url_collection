# 🚀 MAL_URL_COLLECTOR

**MAL_URL_COLLECTOR**는 악성 URL을 수집하고 데이터베이스에 저장하는 Python 기반 웹 크롤러 프로젝트입니다.  
이 프로젝트는 자동화된 방식으로 악성 URL 데이터를 수집하여, 데이터를 MySQL 데이터베이스에 저장합니다.

---

## 📂 **프로젝트 구조**

```
MAL_URL_COLLECTOR/ 
│ 
├── app/ 
│ 
├── db.py # MySQL 연결 및 데이터 삽입 로직 
│ 
├── logger.py # 로그 설정 파일 
│ 
├── crawler.py # 크롤러
│
├── log/ # 크롤러 실행 로그 저장 
│   │ 
│   └── Collection_{date}.log # 일자별 로그 파일
│
├── config/ 
│   │ 
│   ├── .env # 환경 변수 파일 (DB 연결 정보) 
│   │ 
│   └── .env.local # 로컬 환경 변수 파일 (DB 연결 정보) 
│ 
├── requirements.txt # 필요한 Python 패키지 목록 
├── README.md # 프로젝트 설명서 
└── .gitignore # Git 관리에서 제외할 파일 목록
```

---

