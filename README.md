Django 안전교육 자료 생성 앱
사용자 입력을 받아 Gemini API를 호출하여 안전교육 자료(가정통신문, PDF)를 생성하는 Django 애플리케이션입니다.

주요 기능
사용자 입력: 학교급(초/중/고), 산출물(가정통신문/PDF), 테마(화재/일반) 선택
동적 콘텐츠 생성: static/data의 JSON 파일을 기반으로 Gemini API를 호출하여 콘텐츠 생성
프롬프트 엔지니어링: 서버(services/prompt_builder.py)와 클라이언트(static/components/promptBuilder.js)에 동일한 규칙의 프롬프트 빌더 구현
결과 제공: 가정통신문은 인쇄용 HTML로, 교육자료는 PDF(구현 예정)로 제공

기술 스택
백엔드: Django, Gunicorn
AI: Google Gemini API
프론트엔드: Vanilla JavaScript (ESM), HTML, CSS
배포: Docker

실행 방법
1. 환경 설정
프로젝트 루트 디렉토리에 .env 파일을 생성하고 Gemini API 키를 추가합니다.

GEMINI_API_KEY="YOUR_API_KEY_HERE"

주의: .env 파일은 절대 Git에 커밋하지 마세요. .gitignore에 추가하는 것을 권장합니다.

2. 로컬 개발 환경 (가상환경 사용)
# 1. 가상환경 생성 및 활성화
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 2. 의존성 설치
pip install -r requirements.txt

# 3. 데이터베이스 마이그레이션
python manage.py migrate

# 4. 개발 서버 실행
python manage.py runserver

서버 실행 후, 웹 브라우저에서 http://127.0.0.1:8000 로 접속하세요.

3. Docker를 이용한 실행
# 1. Docker 이미지 빌드
docker build -t edu-app-django .

# 2. Docker 컨테이너 실행
# .env 파일의 환경 변수를 컨테이너에 전달합니다.
docker run --rm -p 8000:8000 --env-file .env edu-app-django
컨테이너 실행 후, 웹 브라우저에서 http://127.0.0.1:8000 로 접속하세요.

다음 단계
PDF 생성 구현: weasyprint 또는 다른 라이브러리를 사용하여 PDF 다운로드 기능 활성화
비동기 처리: Celery와 Redis를 도입하여 Gemini API 호출 및 PDF 생성을 비동기 작업으로 전환
프론트엔드 개선: 로딩 상태, 에러 메시지 등 사용자 경험 향상
로깅 및 모니터링: Sentry, ELK Stack 등을 연동하여 운영 환경에서의 안정성 확보