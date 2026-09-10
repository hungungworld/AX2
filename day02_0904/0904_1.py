import streamlit as st
import pandas as pd # 엑셀 데이터 사용
import os

st.title("💱 오늘의 환율 대시보드")
st.caption("아래 데이터는 실제 환율이 아닌 실습용 샘플 데이터입니다.")

# 경로 지정
CSV_PATH = os.path.join(os.path.dirname(__file__), "..", "common", "raw_trade_data.csv")
# (__file__) : 현재 실행 중인 파이썬 파일 자기 자신을 가리킨다.
# ".." : 현재 폴더에서 상위 폴더로 빠져나간다.
# 같은 폴더에 있을 때: CSV_PATH = os.path.join(os.path.dirname(__file__), "raw_trade_data.csv")


# 환율 샘플 데이터
# 딕셔너리로 표 만들기
exchange_data = {   
    '통화' : ["USD", "EUR", "JPY(100엔)", "CNY"],
    '환율' : [1390.5000, 1503.2000, 930.8000, 191.3000],
    '전일대비' : [+5.2, -3.1, +1.0, -0.4],
    }

#1 1) 환율 표 보기
st.subheader("1) 환율 표 보기")
st.write("▶ st.dataframe (상호작용 가능한 표)")

df_exchange_data = pd.DataFrame(exchange_data)

st.dataframe(df_exchange_data)
# st.dataframe(df_exchange_data, use_container_width=False)
# 표 전체 길이 변경: use_container_width=False

st.write("▶ st.table (정적인 표)")
st.table(df_exchange_data)

st.markdown("---")


# 2) 주요 환율 카드 (st.metric(라벨, 현재값, 증감값))
st.subheader("2) 주요 환율 카드 (st.metric)")

# 3칼럼으로 나누기
col1, col2, col3 = st.columns(3)

with col1 :
    st.metric(label="USD/KRW", value="1,4500.5", delta="+5.2")
with col2 :
    st.metric(label="EUR/KRW", value="1,503.2", delta="-3.2")
with col3 :
    st.metric(label="JPY/KRW", value=930.8, delta=+1.2)

st.markdown("---")


# 3) 보너스
st.subheader("3) 보너스: 무역 원본 데이터 미리보기")
st.write("공용 데이터 파일 raw_trade_data.csv를 읽어온 상위 5행입니다.")

# CSV 파일 읽어오기 (encoding: 깨지지 않게 한글 인코딩 진행)
df_trade = pd.read_csv(CSV_PATH, encoding="utf-8")

# 상위 5행 출력
st.dataframe(df_trade.head(5))