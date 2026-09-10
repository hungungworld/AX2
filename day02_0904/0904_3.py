# # 로또 번호 자동 생성기
#lotto v1
#lotto v2
#lotto v3

# # random 모듈을 이용해서 1~45 중 중복 없는 번호 6개를 뽑는다.
# # 자료 구조 set(중복 불가) 사용 <-> list(중복 허용)
# # 버튼을 누르면 5세트를 한번에 생성
# # datetime으로 생성 시간도 함께 보여준다

import streamlit as st
import random
from datetime import datetime

# 1. 교수님 방식대로 set[int]() 사용
def generate_lotto_number() -> list:
    """1~45에서 중복없이 번호 6개 뽑아 정렬된 리스트로 반환""" 
    number = set[int]()  # 정수형(int)만 담는 set 선언
    while len(number) < 6:
        number.add(random.randint(1, 45))
    return sorted(number)

# 2. 번호 대역별 색깔공 이모지를 붙여주는 함수
def format_lotto_ball(num: int) -> str:
    if num <= 10:
        color_ball = "🟡"
    elif num <= 20:
        color_ball = "🔵"
    elif num <= 30:
        color_ball = "🔴"
    elif num <= 40:
        color_ball = "⚫"
    else:
        color_ball = "🟢"
    return f"{color_ball} {num:02d}"  # 02d: 1~9는 01, 02처럼 예쁘게 줄 맞춰 출력


st.title("🎱 로또 번호 자동 생성기")
st.caption("버튼을 누르면 1~45 사이의 중복 없는 번호 6개짜리 세트를 5개 만들어줍니다.")
st.markdown("---")

# 버튼을 눌렀을 때만 아래 내용이 실행되도록 설정
if st.button("🎲 5세트 번호 생성하기"):
    now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    st.write(f"생성 시각: **{now_str}**")

    for set_index in range(1, 6):
        lotto_num = generate_lotto_number()
        

        # 1) [format_lotto_ball(n) for n in lotto_num]
        #    - 뽑힌 숫자 6개를 하나씩 꺼내 색깔공 함수에 넣어 변환한다.
        #    - 변환 결과 예시: ['🟡 03', '🔵 15', '🔴 27', '⚫ 33', '⚫ 38', '🟢 42']
        #
        # 2) "  ".join(...)
        #    - 리스트 형태는 화면에 대괄호([])와 쉼표가 그대로 찍혀 지저분하다.
        #    - join은 리스트 안의 문자열들을 지정한 접착제(여기서는 공백 2칸 "  ")로 이어 붙여 하나의 문장으로 만든다.
        #    - 최종 결과 예시: "🟡 03  🔵 15  🔴 27  ⚫ 33  ⚫ 38  🟢 42"

        # 뽑힌 숫자 6개에 각각 색깔공을 입혀서 한 줄로 합치기
        balls_str = "  ".join([format_lotto_ball(n) for n in lotto_num])
        
        # 화면에 출력
        st.write(f"**{set_index}세트** : {balls_str}")



        # import streamlit as st
# import random
# from datetime import datetime

# def generate_lotto_number() -> list :
#     """1~45에서 중복없이 번호 6개 뽑아 정렬된 리스트로 반환""" 

#     number = set[int]()
#     while len(number) < 6:
#         number.add(random.randint(1,45)) # 1이상 45이하 정수 하나 뽑기
#     return sorted(number) # sorted : 오름차순 정렬


# st.title("🎱 로또 번호 자도 생성기")
# st.caption("버튼을 누르면 1~45 사이의 중복 없는 번호 6개짜리 세트를 5개 만들어줍니다.")
# st.markdown("---")

# st.button("🎲 5세트 번호 생성하기")
# now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
# st.write(f"생성 시각: **{now_str}**")
# st.markdown("---")

# for set_index in range(1,6):
#     lotto_num = generate_lotto_number()
    
#     st.write(f"{set_index}세트 : {lotto_num} ")