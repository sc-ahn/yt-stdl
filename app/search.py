import argparse
from datetime import datetime

import orjson
from googleapiclient.discovery import build

from app.common import LogLevel, ensure_path, get_logger
from app.schema import VideoMetadata
from app.settings import EXAMPLE_DIR, env

logger = get_logger(__name__, LogLevel.INFO)


def search_video_list(keyword: str) -> list[VideoMetadata]:
    youtube = build("youtube", "v3", developerKey=env.API_KEY)

    request = youtube.search().list(
        part="snippet", q=keyword, type="video", maxResults=50
    )
    response = request.execute()
    items = response.get("items", [])
    video_list = []
    for item in items:
        video_list.append(VideoMetadata(**item))

    return video_list


def search_all_videos(
    keyword: str,
    max_pages: int = 5,
    size_per_page: int = 50,
) -> list[VideoMetadata]:
    youtube = build("youtube", "v3", developerKey=env.API_KEY)
    videos = []
    page_token = None

    for _ in range(max_pages):
        request = youtube.search().list(
            part="snippet",
            q=keyword,
            type="video",
            maxResults=size_per_page,
            pageToken=page_token,
        )
        response = request.execute()
        items = response.get("items", [])
        for item in items:
            videos.append(VideoMetadata(**item))
        page_token = response.get("nextPageToken")
        if not page_token:
            break
    return videos


def save_metadata_to_file(
    videos: list[VideoMetadata], filename: str | None = "metadata"
):
    if not filename:
        filename = datetime.now().strftime("%Y%m%d-%H%M%S")
    ensure_path(EXAMPLE_DIR / filename)
    with open(
        EXAMPLE_DIR / filename / f"{filename}-metadata.json", "w", encoding="utf-8"
    ) as f:
        f.write(
            orjson.dumps(
                [video.model_dump() for video in videos], option=orjson.OPT_INDENT_2
            ).decode()
        )


def main(keyword: str, save_file: bool = False, max_pages: int = 3):
    videos = search_all_videos(keyword, max_pages=max_pages)
    for video in videos:
        logger.info(
            "[%s] %s - %s",
            video.id.videoId,
            video.snippet.title,
            video.snippet.channelTitle,
        )
    if save_file:
        save_metadata_to_file(
            videos=videos,
            filename=keyword,
        )


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="YouTube 동영상 검색")
    parser.add_argument("keyword", help="검색할 키워드")
    parser.add_argument("--save", action="store_true", help="검색 결과를 파일로 저장")
    parser.add_argument(
        "--max-pages", type=int, default=3, help="검색할 최대 페이지 수 (기본값: 3)"
    )

    args = parser.parse_args()

    main(keyword=args.keyword, save_file=args.save, max_pages=args.max_pages)
