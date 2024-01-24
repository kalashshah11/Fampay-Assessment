import os
import uuid
from datetime import datetime, timedelta

import django.db
from pymongo import errors as mongoerrors

from googleapiclient import discovery
from googleapiclient import errors
from django.utils import dateparse

from app.models import Video, Thumbnail

i = 0


def youtube_search():
    if os.getenv("GOOGLE_API_KEY") is None or os.getenv("QUERY_TERM") is None or os.getenv("INTERVAL") is None:
        print("Mandatory Env Variables Missing")
        exit()

    apiServiceName = "youtube"
    apiVersion = "v3"
    apiKeys = os.environ["GOOGLE_API_KEY"].split(",")
    global i
    while i < len(apiKeys):
        try:
            youtubeDataApi = discovery.build(serviceName=apiServiceName, version=apiVersion,
                                             developerKey=apiKeys[i])
            videos = youtubeDataApi.search().list(
                part="snippet",
                order="date",
                publishedAfter=(datetime.utcnow() - timedelta(seconds=int(os.getenv("INTERVAL")))).isoformat() + "Z",
                q=os.getenv("QUERY_TERM"),
                type="video",
                maxResults=50
            ).execute()

            for item in videos["items"]:
                try:
                    video = Video(
                        _id=item["id"]["videoId"],
                        id=item["id"]["videoId"],
                        title=item["snippet"]["title"],
                        description=item["snippet"]["description"],
                        publishTime=dateparse.parse_datetime(item["snippet"]["publishTime"]),
                        channelTitle=item["snippet"]["channelTitle"],
                        channelId=item["snippet"]["channelId"],
                    )
                    video.save()
                    video.save(using="mongo")
                    for resolution, thumbnail in item["snippet"]["thumbnails"].items():
                        save_id = uuid.uuid4()
                        thumbnail_obj = Thumbnail(
                            _id=save_id,
                            id=save_id,
                            video=video,
                            url=thumbnail["url"],
                            width=thumbnail["width"],
                            height=thumbnail["height"],
                            resolution=resolution
                        )
                        thumbnail_obj.save()
                        thumbnail_obj.save(using="mongo")
                except django.db.IntegrityError:
                    print("Integrity Error")
                except mongoerrors.BulkWriteError:
                    print("Mongo Bulk Write Error")
            break
        except errors.Error:
            print("Quota Exceeded")
            i += 1
            continue
