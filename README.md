# alarmCapture
streamlit, selenium

## 구성
* htmlForm/
  * 010PAY.html
  * 비선불.html
  * 선불.html
  * 지급대행.html
* pages/
  * 1non_advancePAY.py
  * 2.010PAY.py
  * 3Payout_service.py
  * Board.py
* advancePAY.py
* reMind.py

## 목적
규격화된 정보공유서를 통한 파일오류 및 오탈자 최소화

## 기대효과
* 동일 규격 정보공유서 작성
* 당사 및 가맹점 정보 오탈자 최소화

## 기능
* streamlit 웹 서비스, 사용자 수기입력 최소화
* html 입력값 기입
* selenium 웹 브라우저 캡쳐 및 이미지 저장
* telegramBot API 이미지 전송
