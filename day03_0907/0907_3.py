"""
타이타닉 데이터 필터링, 결측치 정리
1) age(나이)가 35 이상인 승객 필터링
2) 성별로 필터링
3) titanic_cleaned.csv로 저장
실행방법: streamlit run 0907_3.py
"""

import pandas as pd
import streamlit as st

st.title("타이타닉 데이터 필터링 & 결측치 정리")
st.caption("나이·성별 조건으로 필터링 해보고, 결측치를 제거해 새 csv로 저장합니다.")

CSV_PATH = "..\common\Titanic.csv"

try:
    df = pd.read_csv(CSV_PATH)

except FileNotFoundError:
    st.error("❌ Titanic.csv 파일을 찾을 수 없습니다.")
# if error 구문과 동일    

else:
    st.metric("원본 데이터 행 개수", f"{len(df)}행")
    st.markdown("---")


# Age 35세 이상 필터링
st.subheader("1) 나이 35세 이상 승객")
over_35 = df[df["Age"]>=35] # 조건 만족 시: df[True]
st.write(f"나이 35세 이상 승객 수 : **{len(over_35)}명**")

st.dataframe(over_35[["Name", "Sex", "Age"]].head())
# 대괄호 2개 주의

st.markdown("---")

# 성별·여자 남자 필터링 2컬럼 사용
st.subheader("2) 성별 필터링 결과")
female_df = df[df["Sex"] == "female"]
male_df = df[df["Sex"] == "male"]

col1, col2 = st.columns(2)
with col1:
    st.metric("여성 승객 수", f"{len(female_df)}명")
with col2:
    st.metric("남성 승객 수", f"{len(male_df)}명")

st.markdown("---")

# 두 조건을 동시에 만족하는 행 (35세 이상 여성)
st.subheader("3) 35세 이상 & 여성 승객")
over_35_female = df[(df["Age"]>=35) & (df["Sex"] == "female")]
# &는 and, ||는 or
st.write(f"35세 이상 & 여성 승객 수: **{len(over_35_female)}명**")

st.markdown("---")

# Age의 결측치(NaN) 확인 및 dropna 처리
st.subheader("4) Age 결측치 처리")
missing_age_count = df["Age"].isna().sum() # isna()는 결측치면 True 반환
st.write(f"Age 열의 결측치 : {missing_age_count}개")

# subset=["Age"] : Age 열이 결측치인 행만 골라서 제거한다.
df_clean = df.dropna(subset=["Age"])
col1, col2 = st.columns(2)
with col1:
    st.metric("원본 데이터 행 개수", f"{len(df)}행")
with col2:
    st.metric("원본 데이터 행 개수", f"{len(df_clean)}행")

# 정리된 데이터를 csv 파일로 저장
output_path = "Titanic_cleaned.csv"
df_clean.to_csv(output_path, index=False) # 인덱스 없이 가져오기
st.success("파일을 저장했습니다.")
st.dataframe(df_clean.head())