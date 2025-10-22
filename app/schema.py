from typing import Annotated

from pydantic import BaseModel, Field


class Thumbnail(BaseModel):
    url: Annotated[
        str,
        Field(
            description="Thumbnail URL",
            examples=["https://i.ytimg.com/vi/n61ULEU7CO0/default.jpg"],
        ),
    ]
    width: Annotated[int | None, Field(description="Thumbnail Width")] = None
    height: Annotated[int | None, Field(description="Thumbnail Height")] = None


class Thumbnails(BaseModel):
    default: Thumbnail
    medium: Thumbnail
    high: Thumbnail
    standard: Thumbnail | None = None
    maxres: Thumbnail | None = None


class IDMap(BaseModel):
    kind: Annotated[str, Field(description="ID Kind", examples=["youtube#video"])]
    videoId: Annotated[str, Field(description="Video ID", examples=["n61ULEU7CO0"])]


class Snippet(BaseModel):
    publishedAt: Annotated[
        str, Field(description="Publish Date", examples=["2021-12-31T16:30:13Z"])
    ]
    channelId: Annotated[
        str, Field(description="Channel ID", examples=["UCSJ4gkVC6NrvII8umztf0Ow"])
    ]
    title: Annotated[
        str,
        Field(
            description="Video Title",
            examples=["Best of lofi hip hop 2021 ✨ [beats to relax/study to]"],
        ),
    ]
    description: Annotated[
        str,
        Field(
            description="Video Description",
            examples=["Listen on Spotify, Apple music and more ..."],
        ),
    ]
    thumbnails: Thumbnails
    channelTitle: Annotated[
        str, Field(description="Channel Title", examples=["Lofi Girl"])
    ]
    liveBroadcastContent: Annotated[
        str, Field(description="Live Broadcast Content", examples=["none"])
    ]
    publishTime: Annotated[
        str, Field(description="Publish Time", examples=["2021-12-31T16:30:13Z"])
    ]


class VideoMetadata(BaseModel):
    kind: Annotated[str, Field(description="Resource Kind", examples=["youtube#video"])]
    etag: Annotated[
        str,
        Field(
            description="ETag of the resource", examples=["AD00C0RTy-ba-3BqoOT7ZxfEXi4"]
        ),
    ]
    id: IDMap
    snippet: Snippet


class TranscriptSummary(BaseModel):
    video_id: Annotated[str, Field(description="Video ID", examples=["n61ULEU7CO0"])]
    title: Annotated[
        str,
        Field(
            description="Video Title",
            examples=["Best of lofi hip hop 2021 ✨ [beats to relax/study to]"],
        ),
    ]
    language_code: Annotated[
        str, Field(description="Transcript Language", examples=["en"])
    ]
    is_generated: Annotated[
        bool, Field(description="Is Transcript Generated", examples=[True, False])
    ]
    scripts: Annotated[
        list[str],
        Field(
            description="List of Transcript Scripts",
            examples=[
                [
                    "hey how's it going",
                    "i'm here with another video",
                    "this is a sample transcript",
                ]
            ],
        ),
    ]
