# MUSCLE QUEST — 로그인 없는 버전

AI, 회원가입, 로그인, Supabase 없이 실행하는 Streamlit 운동 앱입니다.

## GitHub 저장소
저장소 하나에 `app.py`와 `requirements.txt` 파일을 올리면 됩니다.

## Streamlit 배포
1. Streamlit Community Cloud에서 GitHub 저장소를 연결합니다.
2. Main file path에 `app.py`를 지정합니다.
3. Deploy를 누릅니다.

별도의 Secrets 설정이나 Supabase 프로젝트는 필요하지 않습니다.

## 포함 기능
- 운동 도감과 부위/유형/검색 필터
- 운동 저장소
- 루틴 생성, 운동 추가/삭제/순서 변경
- 세트별 중량, 반복 횟수, 완료 여부 기록
- 날짜별 기록과 최근 30일 훈련 차트
- 근육 중복 분석과 보완 운동 추천
- 근육학 TIP 수집
- 경험치, 레벨, 업적
- JSON 백업 및 복원

## 데이터 저장 주의
로그인과 데이터베이스를 제거했기 때문에 기록은 현재 Streamlit 세션에 저장됩니다. 브라우저를 새로 열거나 세션이 종료되면 기록이 초기화될 수 있습니다. `백업 / 복원` 메뉴에서 JSON 파일을 내려받아 보관하고, 다음에 앱을 열면 복원하세요.
