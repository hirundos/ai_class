import re
from . import image_service

def process_content_for_images(content_text: str) -> str:
    
    # [IMAGE: "설명"] 패턴을 찾는 정규표현식
    def replace_tag_with_image(match):
        image_prompt = match.group(1)
        image_data_base64 = image_service.generate_image_from_prompt(image_prompt)
        return f'<img src="{image_data_base64}" alt="{image_prompt}" style="max-width: 100%; height: auto; border-radius: 8px; margin: 1em 0;">'

    processed_html = re.sub(r'\[IMAGE: ([^\]]+)\]', replace_tag_with_image, content_text)
    
    return processed_html