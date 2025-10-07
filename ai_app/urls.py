from django.urls import path
from . import views
from .api import views as api_views

app_name = 'ai_app'

urlpatterns = [
    # Template-rendering views
    path('', views.index, name='index'),
    path('result/print/<int:request_id>/', views.result_print_view, name='result_print'),

    # API endpoints
    path('api/static-data/<str:theme>/', api_views.get_static_data, name='api_get_static_data'),
    path('api/generate/', api_views.generate_content, name='api_generate'),
    path('api/result/<int:request_id>/', api_views.get_generation_status, name='api_get_status'),
    path('api/generate/field_trip/', api_views.generate_field_trip_content, name='generate_field_trip_content'),
]
