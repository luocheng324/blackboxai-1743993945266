from django.urls import path
from .api.views import ComponentAPIView, FileUploadView

app_name = 'oil_analysis_api'

urlpatterns = [
    path('components/', ComponentAPIView.as_view(), name='component-analysis'),
    path('upload/', FileUploadView.as_view(), name='file-upload'),
]