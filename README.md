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


## Lambda Layer 만들기

Lambda Layer 생성 스크립트는 macOS나 Linux 등에서 실행할 수 있도록 설정되어 있습니다.

터미널에서 다음 프로그램이 설치되어 있는지 확인해 주세요.

* zip / unzip
* AWS CLI (`aws` 명령 입력으로 확인)
* jq

만약 AWS CLI 설정이 안 되어 있다면 [다음 문서](https://docs.aws.amazon.com/ko_kr/cli/latest/userguide/cli-chap-install.html)를 참고해 주세요.

그리고 다음과 같이 스크립트를 실행합니다.

```shell script
TARGET_BUCKET = <S3 bucket 이름>
cd lambda_layer
source ./make_lambda_layer.sh
```

하단에 나오는 Lambda Layer의 ARN을 메모해 주세요. (예: `arn:aws:lambda:(AWS Region):(AWS Account ID):layer:MovieScheduleParser_Layer:(Version number)`)

### Lambda Layer 생성 시 조합 (성공한 내용 기준)

* Python 3.7
* Selenium 3.141.0
* ChromeDriver 2.41 (https://chromedriver.storage.googleapis.com/index.html?path=2.41/)
* Serverless-chrome v1.0.0-55 (https://github.com/adieuadieu/serverless-chrome/releases/tag/v1.0.0-55)
  <br/>(stable version - chromium 69.0.3497.81 버전을 이용)

## Lambda 함수 배포하기

Terraform 및 AWS Provider가 설치되어 있음을 기준으로 합니다.

```shell script
cd lambda_example
terraform init
terraform apply
```

`terraform apply` 명령 실행 시 다음과 같은 순서대로 진행합니다.

* Lambda Layer ARN 입력: (예) `arn:aws:lambda:(AWS Region):(AWS Account ID):layer:MovieScheduleParser_Layer:(Version number)`
* 리전을 입력합니다: 서울 리전인 경우 `ap-northeast-2` 입력 (참고자료)
* 다음 단계 진행을 위해 `yes`를 입력합니다. 

### Lambda 함수 예제

`lambda_example.zip` 파일의 압축을 풀면, 다음과 같이 lambda_example.py 파일을 볼 수 있습니다.

```python
from MovieScheduleParser import parser


def lambda_handler(event, context):

    catch_on_parser = parser.CatchOnScheduleParser('https://www.catchon.co.kr/mp/tv/exclude/ch2.co')
    schedules = catch_on_parser.get_channel_schedule()

    for schedule in schedules:
        print(schedule)

    return schedules
```

이 함수는 Catch On 2 채널의 편성표를 가져와서 반환합니다.