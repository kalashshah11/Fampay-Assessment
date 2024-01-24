from rest_framework.serializers import ModelSerializer
from app.models import Thumbnail, Video


class ThumbnailSerializer(ModelSerializer):
    class Meta:
        model = Thumbnail
        fields = ['resolution', 'url', 'width', 'height', ]


class VideoSerializer(ModelSerializer):
    thumbnails = ThumbnailSerializer(many=True, read_only=True)

    class Meta:
        model = Video
        fields = ('_id', 'title', 'description', 'publishTime', 'channelTitle', 'channelId', 'thumbnails')
