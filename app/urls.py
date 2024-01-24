
from django.urls import path, re_path

from app.views import VideoListAPIView
from app.views import VideoSearchAPIView

urlpatterns = [
    path('videos/', VideoListAPIView.as_view(), name='videos'),
    path('videos/search/', VideoSearchAPIView.as_view(), name='search'),
]