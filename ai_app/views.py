from django.shortcuts import render, get_object_or_404
from .models import GenerationRequest
from .services import content_processor # 👈 새로 만든 서비스 임포트

def index(request):
    """
    메인 페이지를 렌더링합니다.
    """
    return render(request, 'index.html')

def result_print_view(request, request_id):
    req_instance = get_object_or_404(GenerationRequest, pk=request_id)
    context = {
        'result': req_instance
    }
    return render(request, 'result_print.html', context)