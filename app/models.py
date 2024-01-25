from django_elasticsearch_dsl import models
from djongo.models import Model


# Create your models here.

class Video(Model):
    id = models.TextField(primary_key=True)
    _id = models.TextField()
    title = models.TextField()
    description = models.TextField()
    publishTime = models.DateTimeField()
    channelTitle = models.TextField()
    channelId = models.TextField()

    def __str__(self):
        return self.title


class Thumbnail(Model):
    video = models.ForeignKey(Video, on_delete=models.CASCADE, related_name='thumbnails')
    url = models.URLField()
    width = models.IntegerField()
    height = models.IntegerField()
    resolution = models.TextField()

    def __str__(self):
        return self.url
