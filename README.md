# 울엄마해장 입지 평가 매출예측

엑셀 계산 모델을 파이썬 로직으로 변환한 Streamlit 배포용 앱입니다.

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
- `requirements.txt`: Streamlit Cloud 설치 패키지
- `.streamlit/config.toml`: 기본 화면 테마

## 로컬 테스트

```bash
python -m pip install -r requirements.txt
streamlit run streamlit_app.py
```
