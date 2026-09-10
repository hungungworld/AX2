"""
EV 사양 데이터 필터링, 결측치 정리
1) 주행거리(range_km)가 400km 이상인 차량 필터링
2) 구동방식(drivetrain - AWD, FWD, RWD)
    또는 차종(car_body_type - SUV, Sedan) 필터링
3) ev_cleaned.csv로 저장
실행방법: streamlit run 0907_4.py
"""

import pandas as pd
import streamlit as st

st.title("EV 사양 데이터 필터링 & 결측치 정리")
st.caption("구동방식·차종 조건으로 필터링 해보고, 결측치를 제거해 새 csv로 저장합니다.")

CSV_PATH = ("..\common\electric_vehicles_spec_2025.csv")

try:
    df = pd.read_csv(CSV_PATH)

except FileNotFoundError:
    st.error("❌ electric_vehicles_spec_2025.csv 파일을 찾을 수 없습니다.")
# if error 구문과 동일    

else:
    st.metric("원본 데이터 행(차량) 개수", f"{len(df)}행")
    st.markdown("---")


# 1) 주행거리 400km 이상 필터링 (타이타닉의 나이 35세 이상 대응)
st.subheader("1) 주행거리 400km 이상 차량")
over_400km = df[df["range_km"] >= 400]
st.write(f"1회 충전 주행거리 400km 이상 차량 수 : **{len(over_400km)}대**")

# 주요 컬럼만 골라 미리보기
preview_cols = ["brand", "model", "range_km", "battery_capacity_kWh", "top_speed_kmh"]
st.dataframe(over_400km[preview_cols].head())

st.markdown("---")

# 2) 구동 방식별 차량 대수 비교 (타이타닉의 남/녀 성별 대응)
st.subheader("2) 구동 방식(Drivetrain)별 분포")
fwd_df = df[df["drivetrain"] == "FWD"]  # 전륜구동
rwd_df = df[df["drivetrain"] == "RWD"]  # 후륜구동
awd_df = df[df["drivetrain"] == "AWD"]  # 사륜구동

col1, col2, col3 = st.columns(3)
with col1:
    st.metric("전륜구동 (FWD)", f"{len(fwd_df)}대")
with col2:
    st.metric("후륜구동 (RWD)", f"{len(rwd_df)}대")
with col3:
    st.metric("사륜구동 (AWD)", f"{len(awd_df)}대")

st.markdown("---")

# 3) 두 조건을 동시에 만족하는 행 (400km 이상 & 사륜구동 AWD)
st.subheader("3) 주행거리 400km 이상 & 사륜구동(AWD) 차량")
target_df = df[(df["range_km"] >= 400) & (df["drivetrain"] == "AWD")]
st.write(f"두 조건을 모두 만족하는 고성능 전기차 수: **{len(target_df)}대**")

match_cols = ["brand", "model", "range_km", "drivetrain", "acceleration_0_100_s"]
st.dataframe(target_df[match_cols].head())

st.markdown("---")

# 4) 결측치(NaN) 확인 및 dropna 처리
st.subheader("4) 결측치 확인 및 정리")

# 배터리 셀 수는 결측치가 200개가 넘어 컬럼 자체 삭제
# 빈칸이 너무 많아서 쓸모가 적은 number_of_cells 항목(열) 자체를 테이블에서 지워버립니다.
df_dropped = df.drop(columns=["number_of_cells"])

# 토크(torque_nm)와 견인력(towing_capacity_kg) 결측치 확인
# isna()는 결측치면 True 반환
torque_nulls = df["torque_nm"].isna().sum()
towing_nulls = df["towing_capacity_kg"].isna().sum()

st.write(f"• 모터 토크(`torque_nm`) 결측치: **{torque_nulls}개**")
st.write(f"• 견인 용량(`towing_capacity_kg`) 결측치: **{towing_nulls}개**")
st.caption("※ 결측치가 200개가 넘는 `number_of_cells` 열은 분석 대상에서 제외(drop)했습니다.")

# 주요 제원 결측 행 제거
df_clean = df_dropped.dropna(subset=["torque_nm", "towing_capacity_kg", "model"])

col1, col2 = st.columns(2)
with col1:
    st.metric("정제 전 전체 행 개수", f"{len(df)}행")
with col2:
    st.metric("결측치 정제 후 행 개수", f"{len(df_clean)}행")

st.markdown("---")

# 5) 정리된 데이터를 CSV 파일로 저장
st.subheader("5) 정제 데이터 저장")
output_path = "ev_cleaned.csv"
df_clean.to_csv(output_path, index=False)
st.success(f"✅ 정제된 데이터가 '{output_path}' 파일로 저장되었습니다.")
st.dataframe(df_clean.head())