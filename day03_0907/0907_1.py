"""
타이타닉 데이터셋 기초 탐색
pandas head/tail/shape/info/columns 를 사용해서 데이터셋의 기본 정보를
화면에 순서대로 보여주는 streamlit 앱이다.
실행방법: streamlit run 0907_1.py
""" 

import pandas as pd
import streamlit as st
import os # 경로파일
import io # info대신 StringIO 사용위해

st.title("🚢타이타닉 데이터셋 기초 탐색")
st.caption("pandas head/tail/shape/info/columns로 데이터셋 기본 정보를 확인합니다.")

# Titanic.csv 가져오기
CSV_PATH = ("..\\common\\Titanic.csv")

upload_file = st.file_uploader("Titanic_tested.csv 파일을 직접 업로드 할 수 있습니다.(선택사항)", type="csv")

# '비어있지 않니?'라고 물어봄
if upload_file is not None:
    df = pd.read_csv(upload_file)
else:
    try:
        # 사용자가 올리지 않음
        # 내 타이타닉 파일을 읽어 옴
        df = pd.read_csv(CSV_PATH)
    except FileNotFoundError:
        # 파일이 없을 때 사용자가 무엇을 해야 하는지 화면에 안내한다.
        st.error("❌ 타이타닉 파일을 찾을 수가 없습니ㄴ다.")
        st.info("같은 경로에 파일을 업로드 하거나, csv파일을 폴더에 넣고 새로고침 하세요.")
        df = None


if df is not None:
    st.subheader("1) head() : 데이터의 상위 5행 미리보기")
    st.dataframe(df.head(5))
    # st.dataframe(df_head, use_container_width=False)
    # 표 전체 길이 변경: use_container_width=False
    
    st.subheader("2) tail() : 데이터의 하위 5행 미리보기")
    st.dataframe(df.tail(5))
    
    st.subheader("3) shape : 행 개수, 열 개수")
    col1, col2 = st.columns(2)
    with col1:
        st.metric("행 개수", f"{df.shape[0]}개")
    with col2:
        st.metric("열 개수", f"{df.shape[1]}개")

    st.subheader("4) columns : 전체 열(컬럼) 이름 목록")
    # st.write(df.columns) : 표 형태
    st.write(list[str](df.columns))
    # type 생략 가능: st.write(list[](df.columns))

    st.subheader("5) info() : 각 열의 자료형과 결측치(NaN) 여부 요약")
    # df.info 는 값을 리턴하지 않고 터미널(허공)에만 출력만 해주는 함수라서,
    # io.StringIO() 라는 '컴퓨터 메모리 안에 가상의 메모장'에 결과를 받아낸 뒤 그 내용을 text로 보여준다.

    buffer = io.StringIO()
    df.info(buf=buffer) # info()에게 "터미널에 뱉지 말고, 방금 만든 메모장(buffer)에 받아 적어!"라고 시킵니다.
    st.text(buffer.getvalue())
    
    # 위의 buffer 대신 실행 가능
    # info_df = pd.DataFrame({
    #     "타입" : df.dtypes,
    #     "결측치 아닌 개수" : df.notna().sum(),
    #     "결측치 개수" : df.isna().sum(),
    # })

    st.success("기초 정보 확인 끝났습니다. 다음 예제에서 전처리 필터링을 할게요.")