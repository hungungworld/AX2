# 인코딩 자동 감지
# 여러 인코딩("ftf-8-sig", "cp949", "euc-kr") 순서대로 시도
# 내가 쓸 폰트 같은 경로에 있어야 함
# 객실등급별 생존율 막대 그래프 생성 후 그림(.png)으로 저장
# 실행방법: streamlit run 0907_5.py

import os
import matplotlib.pyplot as plt
import pandas as pd
import streamlit as st
from matplotlib import font_manager


st.title("📊 인코딩 자동 감지 + 한글 폰트 막대 그래프 (Titanic 연습)")
st.caption("여러 인코딩을 순서대로 시도해서 파일을 읽고, 객실등급별 생존율을 그래프로 그립니다.")

CSV_PATH = r"C:\Users\user\AX2\day03_0907\Titanic_cleaned.csv"
FONT_PATH = r"C:\Users\user\AX2\day03_0907\font\온글잎 박다현체.ttf"

# 1. 인코딩 순차 시도 함수 정의
def load_csv_with_encodings(file_path):
    encodings = ["utf-8-sig", "cp949", "euc-kr"]

    for enc in encodings:
        try:
            # 투입구(file_path)로 들어온 파일 주소로 찾아가서,
            # 이번 차례의 번역 규칙(enc)으로 표를 읽어봅니다.
            df = pd.read_csv(file_path, encoding=enc)
            st.success(f"성공적으로 파일을 읽었습니다. (적용된 인코딩: `{enc}`)")
            return df
        except UnicodeDecodeError:
            # 글자가 깨져서 읽을 수 없을 때 발생하는 에러(UnicodeDecodeError)를 잡습니다.
            # continue를 통해 다음 인코딩 후보로 넘어가서 다시 시도합니다.
            continue

    # 모든 인코딩 시도가 실패했을 때 예외 발생
    # raise를 사용해 명시적으로 에러(ValueError)를 일으키고 작동을 중단시킵니다.
    raise ValueError(f"지정된 인코딩({encodings})으로 파일을 읽을 수 없습니다: {file_path}")

# 인코딩 자동 감지로 csv 읽기
st.subheader("1) 인코딩 감지")
df = load_csv_with_encodings(CSV_PATH)
st.markdown("---")

# ==============================================================================
# [배경 지식: 왜 0과 1 데이터의 평균이 '비율'이 될까?]
# - Survived 컬럼 값: 사망 = 0, 생존 = 1
# - 예시: 5명 중 3명 생존 시 데이터 -> [1, 0, 1, 1, 0]
# - 평균 구하기: (1 + 0 + 1 + 1 + 0) / 5 = 3 / 5 = 0.6 (즉, 60% 생존)
# -> 따라서 0과 1로 된 컬럼의 평균(.mean())은 곧 전체 중 1의 '비율(생존율)'이 됩니다.
# ==============================================================================

# 1. 등급별 생존율 계산
pclass_survival_rate = (
    df.groupby("Pclass")  # ① 객실 등급(1, 2, 3등급)별로 승객을 끼리끼리 묶음
    ["Survived"]  # ② 다른 정보는 빼고 'Survived(0 또는 1)' 컬럼만 선택
    .mean()  # ③ 각 등급별로 평균(0.629, 0.472 등 비율) 계산
    .sort_index()  # ④ 등급 번호 순서(1등급 -> 2등급 -> 3등급)로 정렬
)

# 2. 사람이 보기 편한 백분율(%) 표로 다듬어서 Streamlit 화면에 출력
st.dataframe(
    (pclass_survival_rate * 100)  # ① 0.629 같은 소수를 62.9%로 바꾸기 위해 100 곱하기
    .round(1)  # ② 소수점 첫째 자리까지만 깔끔하게 반올림
    .rename("생존율(%)")  # ③ 표 제목(컬럼명)을 'Survived'에서 '생존율(%)'로 변경
)
# df_df = st.dataframe((pclass_survival_rate * 100).round(1).rename("생존율(%)"))
# st.write(df_df)

# 차트 그리기

st.markdown("---")
st.subheader("3) 객실 등급별 생존율 막대그래프")
try:
    font_prop = font_manager.FontProperties(fname=FONT_PATH)
    # FONT_PATH에 적힌 폰트 파일(.ttf)을 직접 읽어와서,
    # FontProperties(...): 폰트의 속성(이름, 크기, 스타일 등)을 담아두는 틀(클래스)
    # Matplotlib 그래프 글씨에 적용할 수 있는 '폰트 설정 상자(객체)'로 만듭니다.
    # (그래프에서 한글이 네모 □□ 로 깨지는 문제를 해결하기 위해 사용)

    # matplotlib font_manager에 폰트를 등록하고, 전역 폰트로 설정
    font_manager.fontManager.addfont(FONT_PATH)
    plt.rcParams["font.family"] = font_prop.get_name()
    st.write("온글잎 박다현체 폰트를 적용했습니다.")

    # 폰트 파일이 없으면 FileNotFoundError 가 발생
except FileNotFoundError:
    st.warning("폰트 파일을 찾을 수가 없습니다.")

# ==============================================================================
# [그래프를 그릴 도화지와 액자 준비하기]
# - fig (Figure): 전체 그림판(도화지) 자체를 의미 (나중에 파일로 저장하거나 크기를 조절할 때 사용)
# - ax (Axes): 실제로 막대, 꺾은선, 눈금, 글자 등을 그려 넣는 개별 그래프 영역(액자/좌표평면)
# - figsize=(8, 5): 그래프의 가로, 세로 크기를 인치(inch) 단위로 설정 (가로 8인치, 세로 5인치 비율)
# ==============================================================================
fig, ax = plt.subplots(figsize=(8,5))
(pclass_survival_rate * 100).plot(kind="bar", color="purple", ax=ax)
ax.set_title("객실 등급별 생존율")
ax.set_xlabel("객실등급(Pclass)")
ax.set_ylabel("생존율(%)")

st.pyplot(fig)

# ==============================================================================
# [그래프 이미지(.png) 파일로 저장하기]
# ==============================================================================

# 1. 저장할 경로와 파일명 만들기
# __file__은 현재 실행 중인 파이썬 파일(0907_5.py)을 의미합니다.
# os.path.dirname(__file__) -> 현재 파이썬 파일이 있는 폴더 경로를 가져옵니다.
# os.path.join(..., "chart.png") -> 그 폴더 안에 "chart.png"라는 파일 경로를 완성합니다.
output_png = os.path.join(os.path.dirname(os.path.abspath(__file__)), "chart.png")

# 2. 도화지(fig)를 이미지 파일로 저장하기
# - dpi=300: 해상도 설정 (300이면 인쇄용 수준으로 선명하게 저장됨)
# - bbox_inches="tight": 그래프 바깥쪽 여백을 깔끔하게 잘라내어 글씨가 잘리는 현상 방지
fig.savefig(output_png, dpi=300, bbox_inches="tight")

# 3. Streamlit 화면에 저장이 잘 되었다고 안내 메시지 띄우기 (선택 사항)
st.info(f"그래프가 저장되었습니다: {output_png}")