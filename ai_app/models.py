from django.db import models

class GenerationRequest(models.Model):
    SCHOOL_LEVELS = [("elementary", "초등"), ("middle", "중등"), ("high", "고등")]
    # '현장체험학습' 유형을 선택지에 추가합니다.
    OUTPUT_TYPES = [("notice", "가정통신문"), ("pdf", "교육자료"), ("field_trip", "현장체험학습")]
    STATUS = [("pending","pending"), ("done","done"), ("error","error")]

    # 현장체험학습의 경우 학년 정보로 school_level을 채우므로, null을 허용합니다.
    school_level = models.CharField(
        max_length=20, 
        choices=SCHOOL_LEVELS, 
        help_text="학교급 (초등/중등/고등)", 
        null=True, 
        blank=True
    )
    output_type = models.CharField(
        max_length=20, 
        choices=OUTPUT_TYPES, 
        help_text="산출물 유형"
    )
    
    # choices 옵션을 제거하여 '화재 안전' 같은 테마뿐만 아니라 '국립중앙박물관' 같은 장소명도 자유롭게 저장할 수 있게 합니다.
    theme = models.CharField(
        max_length=100, 
        help_text="안전교육 테마 또는 현장체험학습 장소명"
    )
    
    prompt = models.TextField(
        null=True, 
        blank=True, 
        help_text="AI 모델에 전달된 최종 프롬프트"
    )
    response_text = models.TextField(
        null=True, 
        blank=True, 
        help_text="AI 모델로부터 받은 응답 (HTML 형식)"
    )
    
    status = models.CharField(
        max_length=20, 
        choices=STATUS, 
        default='pending'
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"[{self.get_status_display()}] {self.theme} ({self.get_output_type_display()}) - ID: {self.id}"