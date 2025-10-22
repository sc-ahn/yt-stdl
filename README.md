# YT-STDL

> YouTube SubTitle DownLoader (yt-stdl)

## TL;DR

- 유튜브 자막 다운로드 PoC
  - 자동화 가능
    - Youtube Data API v3, youtube-transcript-api 조합
    - 공식 API는 안정적이지만 사용이 복잡하고 제한사항이 많음, 일 사용량 제한 주의 필요
  - 영상 갯수 대비 수집되는 자막이 많지 않음

## 실행 방법

```bash
make build
make up
make sh

# 검색
./bin/search "검색키워드" [--save] [--max-pages N]

# 자막 다운로드
./bin/subtitle "검색키워드" [--language en|ko|...] [--max-pages N]
```

## 기술적인 부분들

### Youtube Data API v3

> [YouTube > Data API > Search: list](https://developers.google.com/youtube/v3/docs/search/list?hl=ko&_gl=1*w12hkz*_up*MQ..*_ga*MTA0MzM2MTE3Mi4xNzYxMDg4NDI2*_ga_SM8HXJ53K2*czE3NjEwOTIwNDgkbzIkZzAkdDE3NjEwOTI3NjYkajYwJGwwJGgw)

`Youtube Data API v3` 를 사용하여 YouTube 영상 메타데이터를 검색할 수 있습니다.

특정 키워드로 영상 검색 시 영상 ID, 제목, 설명, 채널명, 게시일 등 다양한 메타데이터를 함께 가져올 수 있습니다.

API Key 발급이 필요하며, 일일 할당량 제한이 있습니다.

- 무료, 사용하기 편함, 자동화 쉬움
- 호출시 할당량 비용 100을 사용함, 일일 할당량 기본 10,000
  - 하루에 100번 호출하면 할당량 소진됨
  - 할당량 증가 요청시 [별도의 양식 제출](./example/support/form.pdf)필요
  - 검색결과 한번에 최대 50개 까지 반환
    - 페이지네이션 지원, 다음 페이지 토큰으로 추가 요청 가능
- 공식, 안정성 높음

사용 패턴에 따라 할당량이 빠르게 소진될 수 있으므로 주의가 필요함

## 자막

### YouTube Data API v3

> [YouTube > Data API > Captions: list](https://developers.google.com/youtube/v3/docs/captions/list?_gl=1*155l5bv*_up*MQ..*_ga*MTA0MzM2MTE3Mi4xNzYxMDg4NDI2*_ga_SM8HXJ53K2*czE3NjEwODg0MjUkbzEkZzAkdDE3NjEwODg0NjIkajIzJGwwJGgw)

`YouTube Data API v3` 를 사용하여 자막 정보를 가져오려는경우 `client_secrets.json` 파일 세팅과 OAuth 2.0 인증이 필요합니다.

#### 제한사항 및 특이점: Youtube Data API v3 Captions

- 클라이언트 OAuth 2.0 인증 필요
  - 자동화 번거로움
- 영상의 업로더가 자막 접근을 허용해야함
- 비공개 영상, API 접근제한 자막은 다운로드 불가
- `captions.download` 메서드로 srt 등 원하는 자막 포맷으로 다운로드 가능
- 공식, 안정성 높음

### youtube-transcript-api

[jdepoix/youtube-transcript-api](https://github.com/jdepoix/youtube-transcript-api) 를 사용하면 별도의 인증절차 없이 자막을 가져올 수 있습니다.

YouTube 페이지에서 사용하는 API 엔드포인트를 역공학하여 호출하는 방식입니다.

#### 제한사항 및 특이점: youtube-transcript-api

- 브라우저 자동화도구 필요 없음, 자동화 쉬움
- 비공개 영상 자막 다운로드 불가
- 웹에서 사용하는 API를 이용하므로 YouTube 화면 및 호출구조 변경에 취약
- JSON 형식 데이터 파싱해서 사용
