from django.db.models import Q
from django.shortcuts import render

from rest_framework.generics import ListAPIView
from rest_framework.pagination import PageNumberPagination

from app.documents import VideoDocument
from app.models import Video
from app.serializer import VideoSerializer


# Create your views here.
class StandardResultsSetPagination(PageNumberPagination):
    # Default page size is 10
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 1000


# Create your views here.
class VideoListAPIView(ListAPIView):
    serializer_class = VideoSerializer
    model = Video
    pagination_class = StandardResultsSetPagination

    def get_queryset(self):
        queryset = self.model.objects.all()
        return queryset.order_by('-publishTime')


class VideoSearchAPIView(ListAPIView):
    serializer_class = VideoSerializer
    model = Video
    pagination_class = StandardResultsSetPagination

    def get_queryset(self):
        query = self.request.query_params.get('query')
        if query is not None:
            queryset = VideoDocument.search().query("match", title=query)
            return queryset

        return {}