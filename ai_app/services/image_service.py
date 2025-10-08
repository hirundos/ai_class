# image_service.py

import os
from google import genai
from google.genai import types
import base64

# API 키 설정
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")

# genai.configure 대신 Client 객체 사용
# API 키가 None이거나 비어있을 경우를 대비한 예외 처리
client = None
if GEMINI_API_KEY and GEMINI_API_KEY != "YOUR_DUMMY_API_KEY_FOR_LOCAL_TEST":
    client = genai.Client(api_key=GEMINI_API_KEY)

def generate_image_from_prompt(prompt_text: str) -> str:
    """
    주어진 텍스트 프롬프트로 이미지를 생성하고,
    HTML <img> 태그에 바로 사용할 수 있는 base64 인코딩된 문자열을 반환합니다.
    """
    if not client:
        print(f"--- MOCK IMAGE generation for prompt: {prompt_text} ---")
        grey_pixel_base64 = "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mOM+wAAAgAB/Q33aQAAAABJRU5ErkJggg=="
        return f"data:image/png;base64,{grey_pixel_base64}"

    try:
        print(f"--- API에 전달되는 실제 프롬프트: [{prompt_text}] ---")

        # 공식 문서의 올바른 호출 방식
        response = client.models.generate_content(
            model="gemini-2.0-flash-preview-image-generation",
            contents=[prompt_text],
            config=types.GenerateContentConfig(
                response_modalities=["TEXT", "IMAGE"]
            ),
        )
        for part in response.candidates[0].content.parts:
            if part.text is not None:
                print(part.text)
            elif part.inline_data is not None:
                image_data = part.inline_data.data
                image_base64 = base64.b64encode(image_data).decode('utf-8')

        return f"data:image/png;base64,{image_base64}"

    except Exception as e:
        print(f"Error generating image: {e}")
        return "https://via.placeholder.com/150/CCCCCC/FFFFFF?text=Error"