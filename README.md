# MovieSchedule Parser

[MovieScheduler](https://github.com/rubysoho07/MovieScheduler) 프로젝트에서 영화 편성표 수집 부분만 분리한 프로젝트입니다. 

다음과 같은 것들을 이용합니다. 

* BeautifulSoup
* Selenium
* [ChromeDriver](https://sites.google.com/a/chromium.org/chromedriver/)
* [serverless-chrome](https://github.com/adieuadieu/serverless-chrome)

원래 이 프로젝트의 목적은 AWS Lambda에서 이 프로젝트를 이용해 편성표를 수집하고자 하는 것이었습니다.

기본적으로는 AWS Lambda 환경에서 돌아가는 것을 목표로 하되, 차차 다른 환경에서도 사용할 수 있도록 수정할 예정입니다.

## 동작 결과에 대한 설명

이 라이브러리를 이용하는 경우, 아래 dict 형식의 리스트를 반환합니다.

```json
{
  "start_time": "2019-10-05T15:00:00+09:00",
  "title": "영화 제목",
  "rating": 0
}
```

* `start_time`: 해당 스케줄의 시작 시간 (필수, ISO 8601 형식이며 한국 시간 기준)
* `end_time`: 해당 스케줄의 종료 시간 (없을 수도 있음)
* `title`: 영화 제목 (필수)
* `rating`: 영화에 대한 등급 (필수) - 0인 경우 전체 관람가, 19인 경우 청소년 관람 불가


## 참고 사항

* serverless-chrome 프로젝트의 Chromium 버전이 낮으므로, 이 버전에 맞는 ChromeDriver를 이용해야 합니다.
* 테스트 해 본 환경은 다음과 같습니다.
    * OS: Ubuntu 19.04
    * ChromeDriver 2.39 (https://chromedriver.storage.googleapis.com/index.html?path=2.39/)
    * Serverless-chrome v1.0.0-55 (https://github.com/adieuadieu/serverless-chrome/releases/tag/v1.0.0-55)
      <br/>(stable version - chromium 69.0.3497.81 버전을 이용)