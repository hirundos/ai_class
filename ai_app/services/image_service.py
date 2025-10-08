# image_service.py

import os
from google import genai
from google.genai import types
from PIL import Image
import io 
import base64

# API 키 설정
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")

client = None
if GEMINI_API_KEY and GEMINI_API_KEY != "YOUR_DUMMY_API_KEY_FOR_LOCAL_TEST":
    client = genai.Client(api_key=GEMINI_API_KEY)

def generate_image_from_prompt(prompt_text: str) -> str:
    if not client:
        print(f"--- MOCK IMAGE generation for prompt: {prompt_text} ---")
        grey_pixel_base64 = "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mOM+wAAAgAB/Q33aQAAAABJRU5ErkJggg=="
        return f"data:image/png;base64,{grey_pixel_base64}"

    try:
        print(f"--- API에 전달되는 실제 프롬프트: [{prompt_text}] ---")

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
                image = Image.open(io.BytesIO(image_data))
                resized_image = image.resize((512, 512))
                buffer = io.BytesIO()
                resized_image.save(buffer, format="PNG")
                resized_image_data = buffer.getvalue()
                image_base64 = base64.b64encode(resized_image_data).decode('utf-8')

        return f"data:image/png;base64,{image_base64}"

    except Exception as e:
        print(f"Error generating image: {e}")
        return "https://via.placeholder.com/150/CCCCCC/FFFFFF?text=Error"