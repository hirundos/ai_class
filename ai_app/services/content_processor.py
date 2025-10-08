import re
from . import image_service

def process_content_for_images(content_text: str) -> str:
    """
    콘텐츠 텍스트에서 [IMAGE: "..."] 태그를 찾아 실제 이미지로 변환합니다.

    Args:
        content_text (str): Gemini로부터 받은 원본 텍스트 (HTML 또는 Markdown).

    Returns:
        str: 이미지 태그가 <img> HTML 태그로 변환된 최종 HTML.
    """
    
    # [IMAGE: "설명"] 패턴을 찾는 정규표현식
    # re.sub의 콜백 함수를 사용하여 매치된 각 태그를 처리합니다.
    def replace_tag_with_image(match):
        # 그룹 1: 따옴표 안의 이미지 설명 추출
        image_prompt = match.group(1)
        
        # 이미지 생성 서비스 호출
        image_data_base64 = image_service.generate_image_from_prompt(image_prompt)
        
        # <img> HTML 태그 생성
        return f'<img src="{image_data_base64}" alt="{image_prompt}" style="max-width: 100%; height: auto; border-radius: 8px; margin: 1em 0;">'

    # 닫는 대괄호(])가 나오기 전까지의 모든 문자를 찾도록 수정
    processed_html = re.sub(r'\[IMAGE: ([^\]]+)\]', replace_tag_with_image, content_text)
    
    return processed_html