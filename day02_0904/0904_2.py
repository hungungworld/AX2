# 설문조사 앱 
# 위젯 : 전송버튼, 체크박스, 라디오버튼, 셀렉트박스, 멀티셀렉트박스, 슬라이더, 텍스트입력

import streamlit as st

st.title("📝미니 선호도 조사")
st.caption("위젯을 조작하면 화면 아래 '실시간 응답 요약'이 바로 바뀝니다.")

st.markdown("---")

# 1) 텍스트 입력 위젯 : key를 지정해서 다른 위젯과 이름이 겹치지 않게 한다.
name = st.text_input("1) 이름을 입력하세요.", value="홍길동", key="widget_name")
# age = st.text_input("1) 나이를 입력하세요", value="50", key="widget_age")

# 2) 슬라이드 위젯 : 최소/최대/기본값 지정해 숫자로 선택하게 한다.
age = st.slider(
    "2) 나이를 선택하세요.",
    min_value=10, max_value=80,
    value=25, key="widget_age")

# 3) 라디오 버튼 : 여러 선택지 중에서 하나만 고를 때 사용한다.
job = st.radio(
    "3) 직군을 선택하세요.",
    options=["학생", "직장인", "취준생", "기타"],
    key="widget_job",
    index=3 #"기타"를 기본값으로 설정
)

# 4) 셀렉트박스(드롭다운) : '라디오'와 비슷하지만 목록이 길 때 공간을 공간을 절약할 수 있다.
country = st.selectbox(
    "4) 가장 관심있는 무역 상대국은 ?",
    options=["미국", "독일", "중국", "일본", "베트남"],
    key="widget_country",
)

# 5) 멀티 셀렉트박스 : 여러 개를 동시에 선택할 수 있다.
interests = st.multiselect(
    "5) 관심 있는 데이터 분야를 모두 고르세요.",
    options=["무역통계", "환율", "주가", "날씨", "인구통계"],
    key="widget_interests",
    default=["무역통계"]
)

# 6) 체크박스 : 참/거짓 값 하나를 받을 때
agree = st.checkbox("6) 강의 내용에 만족하시나요?", key="widget_agree")

# 7) 슬라이더 만족도 점수 (1~5점 사이)
score = st.slider(
    "7) 이 강의 만족도 점수(1~5점)",
    min_value=1, max_value=5,
    value=4, key="widget_score"
    )

# score = st.slider(
#     "7) 이 강의 만족도 점수(1~5점)",
#     1,5,4, key="widget_score"
#     )


# 8) 텍스트 영역 : 여러 줄의 입력 필요할 때 자유 의견 입력
feedback = st.text_area(
    "8) 자유롭게 의견을 남겨주세요.",
    key="widget_feedback"
)

# 9) 버튼 : 클릭 여부 (true/false)를 반환한다. 클릭 했을 때만 아래 코드가 실행된다.
submitted = st.button("✅제출하기", key="widget_submit_btn")

st.markdown("---")

# 10) 요약
st.subheader("📊실시간 응답 요약")
# 위젯 값들을 버튼을 누르지 않아도 조작하는 즉시 바로 갱신된다.
# 이름: 홍길동 / 나이: 25세

if submitted: # (if submitted == True)와 동일
    st.write(f"- 이름: **{name}** / 나이: **{age}**")
    st.write(f"- 직군: **{job}** / 관심 국가: **{country}**")

    # interests는 여러 개를 담은 '리스트' 형태: ['무역통계', '환율']
    #    - 대괄호([]) 없이 보기 좋게 이어붙이기 위해 ', '.join() 사용
    #    - 선택 안 해서 빈 리스트면 '선택없음' 출력 (삼항연산자)
    st.write(f"- 관심 분야: **{','.join(interests) if interests else '선택없음'}**")
    st.write(f"- 강의 만족도 여부: **{'만족' if agree else '미선택'}** / 만족도 점수: **{score}점**")
    st.write(f"- 자유 의견: **{','.join(feedback) if feedback else '선택없음'}**")
else:
    st.write("위에 항목을 입력한 뒤 제출하기 버튼을 눌러주세요.")