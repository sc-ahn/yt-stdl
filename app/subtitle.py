import argparse
import time

import orjson
from youtube_transcript_api import (
    FetchedTranscript,
    YouTubeTranscriptApi,
)
from youtube_transcript_api.proxies import WebshareProxyConfig

from app.common import LogLevel, ensure_path, get_logger
from app.schema import TranscriptSummary
from app.search import save_metadata_to_file, search_all_videos
from app.settings import EXAMPLE_DIR, env

logger = get_logger(__name__, LogLevel.INFO)


def reform_transcription(
    title: str, fetched_transcript: FetchedTranscript
) -> TranscriptSummary:
    scripts = []
    for entry in fetched_transcript:
        logger.info(f"entry -> {entry}")
        scripts.append(entry.text)
    return TranscriptSummary(
        video_id=fetched_transcript.video_id,
        title=title,
        language_code=fetched_transcript.language_code,
        is_generated=fetched_transcript.is_generated,
        scripts=scripts,
    )


def main(
    keyword: str,
    language: str = "ko",
    max_pages: int = 3,
    size_per_page: int = 50,
):
    videos = search_all_videos(
        keyword,
        max_pages=max_pages,
        size_per_page=size_per_page,
    )
    save_metadata_to_file(videos, filename=keyword)
    if env.ENABLE_PROXY:
        ytt_api = YouTubeTranscriptApi(
            proxy_config=WebshareProxyConfig(
                proxy_username=env.WEBSHARE_USERNAME,
                proxy_password=env.WEBSHARE_PASSWORD,
            )
        )
    else:
        ytt_api = YouTubeTranscriptApi()
    for video in videos:
        video_id = video.id.videoId
        title = video.snippet.title
        logger.info(f"[{video_id}] {title} 자막 다운로드 시도")
        try:
            fetched_transcript = ytt_api.fetch(
                video_id=video_id,
                languages=[
                    language,
                ],
            )
            logger.info(f"[{video_id}] 자막 다운로드 완료")
            ensure_path(EXAMPLE_DIR / keyword)
            transcript_summary = reform_transcription(title, fetched_transcript)
            with open(
                EXAMPLE_DIR
                / keyword
                / f"{video_id}__{title[:10].replace('.', '')}.json",
                "wb",
            ) as f:
                f.write(
                    orjson.dumps(
                        transcript_summary.model_dump(),
                        option=orjson.OPT_INDENT_2 | orjson.OPT_APPEND_NEWLINE,
                    )
                )
            logger.info(f"[{video_id}] 자막 저장 완료")
            time.sleep(2)
        except Exception as e:
            logger.warning(f"[{video_id}] 자막이 존재하지 않음: {e}")
            continue


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="YouTube 동영상 자막 다운로드")
    parser.add_argument("keyword", help="자막을 다운로드할 동영상을 검색할 키워드")
    parser.add_argument(
        "--size_per_page",
        "-s",
        type=int,
        default=50,
        help="한 페이지당 검색 결과 수 (기본값: 50)",
    )
    parser.add_argument(
        "--max-pages",
        "-m",
        type=int,
        default=3,
        help="검색할 최대 페이지 수 (기본값: 3)",
    )
    parser.add_argument("--language", "-l", default="ko", help="자막 언어 (기본값: ko)")

    args = parser.parse_args()

    main(
        keyword=args.keyword,
        language=args.language,
        max_pages=args.max_pages,
        size_per_page=args.size_per_page,
    )
