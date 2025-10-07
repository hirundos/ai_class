from django.shortcuts import render, get_object_or_404
from .models import GenerationRequest

def index(request):
    """
    메인 페이지를 렌더링합니다.
    """
    return render(request, 'index.html')

def result_print_view(request, request_id):
    """
    생성된 모든 유형의 자료(가정통신문, 교육자료, 현장체험학습)에 대한
    인쇄용 페이지를 렌더링합니다.
    """
    # 요청 ID에 해당하는 생성 결과 객체를 가져옵니다.
    # 객체가 없으면 404 에러를 발생시킵니다.
    req_instance = get_object_or_404(GenerationRequest, pk=request_id)
    
    # 컨텍스트 딕셔너리에 결과 객체를 담아 템플릿으로 전달합니다.
    context = {
        'result': req_instance
    }
    return render(request, 'result_print.html', context)
