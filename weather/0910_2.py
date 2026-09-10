#v1
#v2
#v3


import os
import requests
import streamlit as st
from dotenv import load_dotenv

# 환경 변수 불러오기 (.env 파일)
env_path = os.path.join(os.path.dirname(__file__), "..", ".env")
load_dotenv(dotenv_path=env_path)

WEATHER_API_KEY = os.getenv("OPENWEATHER_API_KEY")
EXCHANGE_API_KEY = os.getenv("EXCHANGE_API_KEY")

# 페이지 기본 설정
st.set_page_config(page_title="멀티 기능 대시보드", page_icon="🌐", layout="wide")

# ==========================================
# ⬅️ 좌측 사이드바 (기능 선택)
# ==========================================
st.sidebar.header("⚙️ 메뉴 선택")
menu = st.sidebar.radio("원하는 서비스를 선택하세요:", ("🌤️ 실시간 날씨 조회", "💱 실시간 환율 조회"))

# ==========================================
# 🌤️ 1. 날씨 조회 화면
# ==========================================
if menu == "🌤️ 실시간 날씨 조회":
    st.title("🌤️ 실시간 날씨 조회 대시보드")
    st.write("전 세계 도시의 현재 날씨를 확인합니다.")
    
    input_mode = st.sidebar.radio("도시 입력 방식:", ("목록에서 선택", "직접 입력"))
    unit_option = st.sidebar.selectbox("온도 단위:", ("섭씨 (°C)", "화씨 (°F)"))
    
    unit_param = "metric" if unit_option == "섭씨 (°C)" else "imperial"
    unit_symbol = "°C" if unit_option == "섭씨 (°C)" else "°F"
    
    city_query = ""
    if input_mode == "목록에서 선택":
        city_options = {
            "로스앤젤레스 (Los Angeles, US)": "Los Angeles,US",
            "뉴욕 (New York, US)": "New York,US",
            "서울 (Seoul, KR)": "Seoul,KR",
            "도쿄 (Tokyo, JP)": "Tokyo,JP",
            "런던 (London, GB)": "London,GB",
            "마인츠 (Mainz, DE)": "Mainz,DE"
        }
        selected_label = st.selectbox("도시 선택:", list(city_options.keys()))
        city_query = city_options[selected_label]
    else:
        city_query = st.text_input("도시 영문 입력 (예: Los Angeles, Mainz):", "Los Angeles")

    if st.button("날씨 조회하기"):
        if not WEATHER_API_KEY:
            st.error("OPENWEATHER_API_KEY가 설정되지 않았습니다.")
        elif not city_query.strip():
            st.warning("도시 이름을 입력해주세요.")
        else:
            search_city = city_query.strip().replace(" ", "").lower() if input_mode == "직접 입력" else city_query
            url = f"https://api.openweathermap.org/data/2.5/weather?q={search_city}&appid={WEATHER_API_KEY}&units={unit_param}&lang=kr"
            
            try:
                response = requests.get(url)
                if response.status_code != 200 and input_mode == "직접 입력" and " " in city_query:
                    retry_city = city_query.strip().replace(" ", "_")
                    url = f"https://api.openweathermap.org/data/2.5/weather?q={retry_city}&appid={WEATHER_API_KEY}&units={unit_param}&lang=kr"
                    response = requests.get(url)
                    
                data = response.json()
                if response.status_code == 200:
                    st.success(f"**{data['name']}, {data['sys']['country']}**의 현재 날씨입니다.")
                    col1, col2, col3 = st.columns(3)
                    col1.metric("현재 온도", f"{data['main']['temp']} {unit_symbol}")
                    col2.metric("체감 온도", f"{data['main']['feels_like']} {unit_symbol}")
                    col3.metric("습도", f"{data['main']['humidity']} %")
                    st.write(f"- **날씨 상태**: {data['weather'][0]['description']}")
                    st.write(f"- **풍속**: {data['wind']['speed']} m/s")
                else:
                    st.error(f"조회 실패: {data.get('message', '알 수 없는 오류')}")
            except Exception as e:
                st.error(f"오류 발생: {e}")


# ==========================================
# 💱 2. 환율 조회 화면 (수정본)
# ==========================================
else:
    st.title("💱 실시간 환율 조회 대시보드")
    st.write("ExchangeRate-API를 이용해 기준 통화 대비 실시간 환율을 확인합니다.")
    
    # 기본값을 USD로 설정하면 1 USD = 1,3xx KRW 형태로 직관적으로 볼 수 있습니다.
    base_currency = st.sidebar.selectbox("기준 통화 (Base):", ("USD", "KRW", "EUR", "JPY", "GBP"), index=0)
    target_currency = st.sidebar.selectbox("조회할 상대 통화:", ("KRW", "USD", "EUR", "JPY", "CNY"), index=0)
    amount = st.sidebar.number_input("금액:", min_value=1.0, value=1.0, step=1.0)

    if st.button("환율 조회하기"):
        if not EXCHANGE_API_KEY:
            st.error("EXCHANGE_API_KEY가 `.env` 파일에 설정되지 않았습니다.")
        else:
            url = f"https://v6.exchangerate-api.com/v6/{EXCHANGE_API_KEY}/latest/{base_currency}"
            
            try:
                response = requests.get(url)
                data = response.json()
                
                if response.status_code == 200 and data["result"] == "success":
                    rates = data["conversion_rates"]
                    if target_currency in rates:
                        exchange_rate = rates[target_currency]
                        converted_amount = amount * exchange_rate
                        
                        st.success("실시간 환율 정보를 성공적으로 불러왔습니다.")
                        
                        col1, col2 = st.columns(2)
                        
                        # 환율 숫자가 매우 작을 수 있으므로(KRW 기준 등) 조건에 따라 소수점 자릿수 동적 처리
                        rate_format = f"{exchange_rate:,.4f}" if exchange_rate < 1 else f"{exchange_rate:,.2f}"
                        
                        col1.metric("적용 환율", f"1 {base_currency} = {rate_format} {target_currency}")
                        col2.metric(f"환산 금액 ({amount:,.0f} {base_currency})", f"{converted_amount:,.2f} {target_currency}")
                    else:
                        st.error(f"대상 통화({target_currency})의 환율 정보를 찾을 수 없습니다.")
                else:
                    st.error("환율 정보를 불러오는 데 실패했습니다. API 키를 확인해주세요.")
            except Exception as e:
                st.error(f"서버 요청 중 오류가 발생했습니다: {e}")