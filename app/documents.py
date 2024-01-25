from django_elasticsearch_dsl import Document, fields
from django_elasticsearch_dsl.registries import registry

from .models import Video, Thumbnail


@registry.register_document
class ThumbnailDocument(Document):

    class Index:
        name = 'thumbnail'

    settings = {
        'number_of_shards': 1,
        'number_of_replicas': 0
    }

    class Django:
        model = Thumbnail
        fields = [
            'resolution', 'url', 'width', 'height'
        ]


@registry.register_document
class VideoDocument(Document):
    # thumbnails = fields.ListField(ThumbnailDocument)

    class Index:
        name = 'video'

    settings = {
        'number_of_shards': 1,
        'number_of_replicas': 0
    }

    class Django:
        model = Video
        fields = [
            'title',
            'description',
            'publishTime',
            'channelTitle',
            'channelId',
            # 'thumbnails'
        ]
