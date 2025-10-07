import json
import os
from django.http import JsonResponse, HttpResponseNotFound
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings

from ..models import GenerationRequest
from ..services import prompt_builder, gemini_service

@require_http_methods(["GET"])
def get_static_data(request, theme):
    """
    선택된 테마에 해당하는 static JSON 파일을 반환합니다. (기존 기능)
    """
    allowed_themes = ['fire_safety', 'general_safety']
    if theme not in allowed_themes:
        return JsonResponse({'error': 'Invalid theme specified'}, status=400)

    file_path = os.path.join(settings.BASE_DIR, 'ai_app', 'static', 'data', f'{theme}.json')
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        return JsonResponse(data)
    except FileNotFoundError:
        return HttpResponseNotFound(f'Data for theme "{theme}" not found.')
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


@csrf_exempt
@require_http_methods(["POST"])
def generate_content(request):
    """
    안전교육 콘텐츠 생성 요청을 처리합니다. (기존 기능)
    """
    try:
        data = json.loads(request.body)
        school_level = data.get('school_level')
        output_type = data.get('output_type')
        theme = data.get('theme')

        if not all([school_level, output_type, theme]):
            return JsonResponse({'error': 'Missing required parameters'}, status=400)
        
        json_path = os.path.join(settings.BASE_DIR, 'ai_app', 'static', 'data', f'{theme}.json')
        with open(json_path, 'r', encoding='utf-8') as f:
            safety_data = json.load(f)

        prompt = prompt_builder.build_prompt(school_level, output_type, theme, safety_data)

        req_instance = GenerationRequest.objects.create(
            school_level=school_level, output_type=output_type,
            theme=theme, prompt=prompt, status='pending'
        )

        try:
            response_text = gemini_service.call_gemini(prompt)
            req_instance.response_text = response_text
            req_instance.status = 'done'
            req_instance.save()

            return JsonResponse({
                'id': req_instance.id,
                'status': 'done',
                'result_text': response_text,
                'output_type': output_type,
            })

        except Exception as e:
            req_instance.status = 'error'
            req_instance.response_text = str(e)
            req_instance.save()
            return JsonResponse({'id': req_instance.id, 'status': 'error', 'error': 'Failed to generate content.'}, status=500)

    except Exception as e:
        return JsonResponse({'error': 'An internal server error occurred.'}, status=500)

@csrf_exempt
@require_http_methods(["POST"])
def generate_field_trip_content(request):
    """
    현장체험학습 자료 생성 요청을 처리합니다. (신규 기능)
    """
    try:
        data = json.loads(request.body)
        grade = data.get('grade')
        location = data.get('location')

        if not all([grade, location]):
            return JsonResponse({'error': '학년과 장소를 모두 입력해야 합니다.'}, status=400)
        
        if not location.strip():
             return JsonResponse({'error': '장소를 입력해주세요.'}, status=400)

        prompt = prompt_builder.build_field_trip_prompt(grade, location)
        
        # 학년을 학교급으로 변환하여 저장 (DB 정리를 위해)
        try:
            grade_num = int(grade)
            if 1 <= grade_num <= 6: school_level = 'elementary'
            elif 7 <= grade_num <= 9: school_level = 'middle'
            else: school_level = 'high'
        except (ValueError, TypeError):
            school_level = None # 학년이 숫자가 아닐 경우

        req_instance = GenerationRequest.objects.create(
            school_level=school_level,
            output_type='field_trip',
            theme=location, # theme 필드에 장소명을 저장
            prompt=prompt,
            status='pending'
        )

        try:
            response_text = gemini_service.call_gemini(prompt)
            req_instance.response_text = response_text
            req_instance.status = 'done'
            req_instance.save()

            return JsonResponse({
                'id': req_instance.id,
                'status': 'done',
                'result_text': response_text
            })

        except Exception as e:
            req_instance.status = 'error'
            req_instance.response_text = str(e)
            req_instance.save()
            print(f"Error during field trip generation: {e}")
            return JsonResponse({'id': req_instance.id, 'status': 'error', 'error': '자료 생성에 실패했습니다.'}, status=500)

    except Exception as e:
        print(f"An unexpected error occurred in field trip API: {e}")
        return JsonResponse({'error': '서버 내부 오류가 발생했습니다.'}, status=500)


@require_http_methods(["GET"])
def get_generation_status(request, request_id):
    """
    (비동기 처리 시 사용) 생성 요청의 현재 상태를 반환합니다. (기존 기능)
    """
    try:
        req_instance = GenerationRequest.objects.get(pk=request_id)
        response_data = {
            'id': req_instance.id,
            'status': req_instance.status,
            'result_text': req_instance.response_text if req_instance.status == 'done' else None,
        }
        return JsonResponse(response_data)
    except GenerationRequest.DoesNotExist:
        return JsonResponse({'error': 'Request not found'}, status=404)

