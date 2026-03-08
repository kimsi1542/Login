# ✈ 여행 일정 관리 앱 (TravelApp) - Backend

이 프로젝트는 캡스톤 디자인 졸업 작품의 백엔드 서버입니다.

## 🛠 Tech Stack
* **Language:** Python 3.12
* **Framework:** Django 6.0.3 + Django REST Framework
* **Database:** MySQL
* **Auth:** Token Authentication

## 🚀 시작하기 (Setup)
1. **가상환경 생성 및 실행**
   ```bash
   python -m venv .venv
   source .venv/Scripts/activate # Windows 기준
2. 필수 라이브러리 설치
pip install -r requirements.txt
3.  DB 연동
MySQL에 rogin_db 데이터베이스를 생성.
Login/settings.py에서 자신의 MySQL 비밀번호로 수정.
4. 테이블 생성 및 서버 실행
python manage.py migrate
python manage.py runserver
5. 회원가입 및 로그인
회원가입 : POST /api/users/register/
로그인 : POST /api/users/login/