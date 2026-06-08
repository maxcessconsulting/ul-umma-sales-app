# 울엄마해장 입지 평가 매출예측

엑셀 계산 모델을 파이썬 로직으로 변환한 Streamlit 배포용 MVP 앱입니다.

## 현재 포함 업종

- 음식점 / 해장국
- 피자
- 치킨

첫 화면의 업종 선택 박스에서 업종을 선택하면 해당 업종의 기본 입력값과 보정 계산 로직이 적용됩니다.

## Streamlit Cloud 배포 방법

1. GitHub에 새 저장소를 만듭니다.
2. 이 폴더 안의 파일을 저장소 루트에 업로드합니다.
3. Streamlit Cloud에서 `Create app`을 누릅니다.
4. 저장소, 브랜치, 앱 파일을 선택합니다.
5. 앱 파일 경로는 아래처럼 지정합니다.

```text
streamlit_app.py
```

배포가 끝나면 `https://...streamlit.app` 형태의 공유 링크가 생성됩니다.

## 파일 구성

- `streamlit_app.py`: 웹 화면
- `pure_model.py`: 엑셀 없이 동작하는 파이썬 계산 로직
- `mvp_industries.py`: MVP 업종 선택, 업종별 기본값, 업종별 보정계수
- `requirements.txt`: Streamlit Cloud 설치 패키지
- `.streamlit/config.toml`: 기본 화면 테마

## MVP 기준

피자와 치킨은 각 엑셀 파일의 기본 결과값에 맞춰 보정계수를 적용한 MVP 계산기입니다.
정식 버전에서는 각 업종의 세부 기준표와 수식을 `pizza.py`, `chicken.py`처럼 별도 계산기로 완전 분해하는 방식으로 고도화합니다.

## 로컬 테스트

```bash
python -m pip install -r requirements.txt
streamlit run streamlit_app.py
```
