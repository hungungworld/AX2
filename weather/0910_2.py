import os
import requests
import streamlit as st
from dotenv import load_dotenv

# ==========================================
# 0. 환경 변수 및 페이지 설정 (절대 경로 추적)
# ==========================================
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
env_path = os.path.join(parent_dir, ".env")

load_dotenv(dotenv_path=env_path)
OPENWEATHER_API_KEY = os.getenv("OPENWEATHER_API_KEY")

st.set_page_config(
    page_title="실시간 날씨 및 추천 옷차림 조회",
    page_icon="🌤️",
    layout="wide"
)

# 모바일 및 PC 반응형 레이아웃 강화 CSS
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@300;400;500;700&display=swap');

html, body, [class*="css"] {
    font-family: 'Noto Sans KR', sans-serif;
}

.main-title {
    font-weight: 700;
    color: #1E293B;
    text-align: center;
    margin-bottom: 5px;
    font-size: 2.1rem;
}

.sub-title {
    color: #64748B;
    text-align: center;
    margin-bottom: 25px;
    font-size: 1rem;
}

@keyframes sunGlow {
    0% { box-shadow: 0 10px 25px -5px rgba(14, 165, 233, 0.4); }
    50% { box-shadow: 0 15px 35px -5px rgba(251, 191, 36, 0.7); }
    100% { box-shadow: 0 10px 25px -5px rgba(14, 165, 233, 0.4); }
}

.weather-card-sunny {
    background: linear-gradient(135deg, #0EA5E9 0%, #0284C7 100%);
    padding: 25px;
    border-radius: 20px;
    color: white;
    text-align: center;
    margin-top: 20px;
    animation: sunGlow 3s infinite;
}

.weather-card-rainy {
    background: linear-gradient(135deg, #475569 0%, #1E293B 100%);
    padding: 25px;
    border-radius: 20px;
    color: white;
    box-shadow: 0 10px 25px -5px rgba(71, 85, 105, 0.4);
    text-align: center;
    margin-top: 20px;
}

.clothes-box {
    background-color: #F8FAFC;
    border: 2px solid #E2E8F0;
    padding: 20px;
    border-radius: 15px;
    color: #334155;
    margin-top: 20px;
}
</style>
""", unsafe_allow_html=True)

st.markdown("<h1 class='main-title'>🌤️ 실시간 날씨 & 맞춤 옷차림 추천</h1>", unsafe_allow_html=True)
st.markdown("<p class='sub-title'>대소문자 및 띄어쓰기 관계없이 도시명을 입력해 실시간 날씨와 의류 추천을 확인하세요.</p>", unsafe_allow_html=True)

# 글로벌 주요 도시 리스트 (자동완성 및 띄어쓰기 교정용)
POPULAR_CITIES = [
    "Seoul", "Busan", "Incheon", "Daegu", "Jeju", 
    "Tokyo", "Osaka", "San Francisco", "New York", 
    "London", "Paris", "Sydney", "Singapore", "Hong Kong", "Los Angeles", "Rome"
]

if not OPENWEATHER_API_KEY:
    st.error("⚠️ `OPENWEATHER_API_KEY`를 찾을 수 없습니다. `.env` 파일 설정을 확인해주세요.")
else:
    # 모바일/PC 반응형 컬럼 배치 (화면이 작아지면 자동으로 세로 정렬)
    col_w1, col_w2 = st.columns([3, 1], gap="medium")
    
    with col_w1:
        city_input = st.text_input("조회할 도시 이름 (예: san francisco, seoul)", value="Seoul")
        
        # 띄어쓰기 및 대소문자 무관하게 실시간 매칭되는 추천 검색어 렌더링
        if city_input:
            query_clean = city_input.replace(" ", "").lower()
            matched_cities = [c for c in POPULAR_CITIES if query_clean in c.replace(" ", "").lower()]
            if matched_cities:
                st.caption(f"💡 추천 검색어: **{', '.join(matched_cities[:5])}**")

    with col_w2:
        # 모바일 화면 간격 맞춤용 마크다운
        st.markdown("<div style='height: 28px;' class='mobile-space'></div>", unsafe_allow_html=True)
        search_btn = st.button("조회하기", type="primary", use_container_width=True)

    if search_btn or city_input:
        # 1. 띄어쓰기나 대소문자 차이로 인한 API 오류 방지 처리 (입력값 정제)
        raw_query = city_input.strip()
        
        # 사용자가 'sanfrancisco'처럼 띄어쓰기를 빼고 입력했을 때 'San Francisco'로 자동 교정해주는 로직
        formatted_query = raw_query
        for city in POPULAR_CITIES:
            if raw_query.replace(" ", "").lower() == city.replace(" ", "").lower():
                formatted_query = city
                break

        weather_url = f"https://api.openweathermap.org/data/2.5/weather?q={formatted_query}&appid={OPENWEATHER_API_KEY}&units=metric&lang=kr"
        
        try:
            res = requests.get(weather_url, timeout=10)
            w_data = res.json()
            
            if res.status_code == 200:
                c_name = w_data.get("name", formatted_query)
                temp = w_data["main"]["temp"]
                feels_like = w_data["main"]["feels_like"]
                humidity = w_data["main"]["humidity"]
                desc = w_data["weather"][0]["description"]
                wind_speed = w_data["wind"]["speed"]
                
                if "비" in desc or "rain" in desc.lower():
                    card_class = "weather-card-rainy"
                    weather_icon = "🌧️"
                else:
                    card_class = "weather-card-sunny"
                    weather_icon = "☀️"
                
                # 기온별 추천 옷차림 로직
                if temp >= 28:
                    clothes_tip = "민소매, 반팔, 반바지, 원피스, 린넨 소재의 시원한 옷"
                    clothes_emoji = "🎽 🩳 🪭"
                elif temp >= 23:
                    clothes_tip = "반팔, 얇은 셔츠, 면바지, 스커트"
                    clothes_emoji = "👕 👖"
                elif temp >= 20:
                    clothes_tip = "얇은 가디건, 긴팔 티셔츠, 면바지, 슬랙스"
                    clothes_emoji = "🧶 👔"
                elif temp >= 17:
                    clothes_tip = "니트, 가디건, 후드티, 야상, 가볍고 편안한 재킷"
                    clothes_emoji = "🧥 🧢"
                elif temp >= 12:
                    clothes_tip = "트렌치코트, 자켓, 셔츠, 가벼운 니트, 청바지"
                    clothes_emoji = "🧥 👖"
                elif temp >= 5:
                    clothes_tip = "코트, 가벼운 패딩, 스카프, 히트텍"
                    clothes_emoji = "🧣 🧥"
                else:
                    clothes_tip = "두꺼운 패딩, 목도리, 장갑, 기모 제품, 방한용품 필수"
                    clothes_emoji = "🧣 🧤 🧊"

                if "비" in desc or "rain" in desc.lower():
                    clothes_tip += " + ☔ 우산을 꼭 챙기세요!"

                st.markdown(f"""
                <div class="{card_class}">
                    <p style="font-size: 1.05rem; opacity: 0.9; margin-bottom: 5px;">현재 날씨 정보</p>
                    <h2 style="font-size: 2rem; font-weight: 700; margin: 10px 0px;">
                        {weather_icon} {c_name}의 날씨: <span style="color: #FBBF24;">{temp:.1f}°C</span>
                    </h2>
                    <p style="font-size: 1.05rem; margin-top: 10px; text-transform: capitalize;">
                        상태: {desc} (체감 온도: {feels_like:.1f}°C)
                    </p>
                    <p style="font-size: 0.9rem; opacity: 0.9; margin-top: 5px;">
                        습도: {humidity}% | 풍속: {wind_speed} m/s
                    </p>
                </div>
                """, unsafe_allow_html=True)

                st.markdown(f"""
                <div class="clothes-box">
                    <h3 style="margin-top: 0px; color: #1E293B; font-size: 1.2rem;">👗 기온별 맞춤 추천 옷차림</h3>
                    <p style="font-size: 1.2rem; margin: 10px 0px;">{clothes_emoji}</p>
                    <p style="font-size: 1rem; font-weight: 500; margin-bottom: 0px;">
                        {clothes_tip}
                    </p>
                </div>
                """, unsafe_allow_html=True)

            else:
                st.error(f"도시를 찾을 수 없거나 데이터를 불러오지 못했습니다. (입력값: {city_input}) 올바른 영문 도시명을 입력해주세요.")
        except Exception as e:
            st.error(f"서버 요청 중 오류가 발생했습니다: {e}")