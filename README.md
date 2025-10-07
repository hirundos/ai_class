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