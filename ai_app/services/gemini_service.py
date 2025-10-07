import os
import google.generativeai as genai
import markdown # 응답을 HTML로 변환하기 위해 추가

# 중요: 이 키는 절대로 소스 코드에 하드코딩하지 마세요.
# 환경 변수, Docker secrets, 또는 클라우드 비밀 관리 서비스를 사용하세요.
os.environ.get('GEMINI_API_KEY')
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")

# 로컬 개발 시, 실제 API 키가 없다면 아래 주석을 풀고 더미 키를 사용하세요.
#if not GEMINI_API_KEY:
#    GEMINI_API_KEY = "YOUR_DUMMY_API_KEY_FOR_LOCAL_TEST"

genai.configure(api_key=GEMINI_API_KEY)

def call_gemini(prompt, timeout=60):
    """
    주어진 프롬프트를 사용하여 Gemini API를 호출하고, 텍스트 응답을 반환합니다.
    실제 API 호출 대신 목(mock) 데이터를 반환하여 API 키 없이도 테스트할 수 있도록 합니다.
    
    Args:
        prompt (str): Gemini 모델에 전달할 프롬프트.
        timeout (int): API 호출 타임아웃 시간 (초).

    Returns:
        str: 생성된 콘텐츠 텍스트.
    """
    # 실제 API 키가 설정되어 있지 않으면, 개발 및 테스트를 위한 목(mock) 응답을 반환합니다.
    if not GEMINI_API_KEY or GEMINI_API_KEY == "YOUR_DUMMY_API_KEY_FOR_LOCAL_TEST":
        print("--- WARNING: GEMINI_API_KEY is not set. Returning mock data. ---")
        # 가정통신문(notice) 형식의 목 응답 (HTML)
        if "가정통신문" in prompt:
            mock_html_response = """
            <h1>화재 안전 가정통신문</h1>
            <p><strong>학부모님께,</strong></p>
            <p>항상 학교 교육에 깊은 관심을 보여주시는 학부모님께 감사드립니다. 건조한 날씨가 계속되면서 화재 위험이 커지고 있습니다. 이에 본교에서는 학생들의 안전을 위해 화재 예방 및 대피 요령에 대한 교육을 실시하였습니다. 가정에서도 우리 아이들이 안전 수칙을 잘 숙지하고 실천할 수 있도록 지도 부탁드립니다.</p>
            
            <h2>핵심 안전 수칙</h2>
            <ul>
                <li>불을 발견하면 큰 소리로 "불이야!"라고 외치고 주변에 알립니다.</li>
                <li>젖은 수건으로 코와 입을 막고, 최대한 낮은 자세로 기어서 대피합니다.</li>
                <li>승강기 대신 반드시 계단을 이용합니다.</li>
            </ul>

            <h2>가정에서의 지도 방법</h2>
            <p>자녀와 함께 집안의 소화기 위치를 확인하고, 실제 화재 상황을 가정한 대피 연습을 해보는 것이 큰 도움이 됩니다. '우리 집 대피 지도'를 함께 그려보는 활동도 좋습니다.</p>
            
            <p>학교에서도 학생들의 안전을 최우선으로 생각하며, 지속적인 안전교육을 실시하겠습니다. 감사합니다.</p>
            <p style="text-align: center;"><strong>- OOO 학교장 드림 -</strong></p>
            """
            return mock_html_response
        # PDF 형식의 목 응답 (Markdown)
        else:
            mock_md_response = """
            # 🔥 화재 발생 시 대피 요령
            
            ## 학습 목표
            1. 화재 발생 시 초기 행동 요령을 알 수 있다.
            2. 안전하게 대피하는 방법을 설명할 수 있다.

            ## 핵심 내용
            ### 1. 불 발견 시!
            - 큰 소리로 "불이야!" 외치기
            - 화재 경보기 누르기
            
            ### 2. 대피 방법
            - 젖은 수건으로 코와 입 막기
            - 낮은 자세로 기어서 이동하기
            - 승강기는 절대 금물! 계단 이용하기

            ## 활동지: 우리 집 대피 계획
            - 우리 집에서 불이 났을 때 어디로 대피할지 가족과 함께 이야기해보고, 대피 경로를 그려봅시다.
            
            ## 정리
            - 화재 시 가장 중요한 것은 '대피 먼저'입니다.
            """
            return markdown.markdown(mock_md_response)


    # --- 실제 Gemini API 호출 로직 ---
    # 실제 운영 시에는 이 로직이 실행됩니다.
    try:
        model = genai.GenerativeModel('gemini-2.0-flash')
        response = model.generate_content(prompt)

        return response.text

    except Exception as e:
        # 실제 환경에서는 더 정교한 예외 처리 및 로깅이 필요합니다.
        # (예: 타임아웃, API 할당량 초과, 인증 오류 등)
        print(f"An error occurred while calling Gemini API: {e}")
        raise  # 예외를 다시 발생시켜 상위 핸들러가 처리하도록 함
