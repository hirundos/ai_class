# 1. 베이스 이미지 설정 (Python 3.11 사용)
FROM python:3.11-slim

# 2. 환경 변수 설정
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# 3. 작업 디렉토리 설정
WORKDIR /app

# 4. 시스템 패키지 설치 (필요시)
# WeasyPrint 같은 PDF 라이브러리는 Pango, Cairo 등의 시스템 의존성이 필요할 수 있습니다.
# RUN apt-get update && apt-get install -y ...

# 5. requirements.txt 복사 및 의존성 설치
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 6. 프로젝트 소스 코드 복사
COPY . .

# 7. Gunicorn 실행
# 프로젝트 이름이 project_settings이므로 wsgi 모듈 경로는 project_settings.wsgi 입니다.
# 8000번 포트를 외부에 노출합니다.
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "project_settings.wsgi:application"]
