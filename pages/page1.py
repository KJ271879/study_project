import streamlit as st
import requests

st.title("날씨 기반 옷차림 추천 앱")

API_KEY = "여기에_발급받은_API_키_입력"  # OpenWeatherMap API 키 넣기

def get_weather(city):
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric&lang=kr"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        return None

def recommend_clothes(temp, weather_desc):
    if temp >= 28:
        return "반팔, 반바지, 샌들 추천! 시원하게 입으세요."
    elif 20 <= temp < 28:
        return "얇은 긴팔, 면바지 또는 청바지 추천."
    elif 10 <= temp < 20:
        return "가벼운 자켓이나 니트, 청바지 입기 좋아요."
    elif 0 <= temp < 10:
        return "코트, 두꺼운 니트, 목도리 착용하세요."
    else:
        return "패딩과 두꺼운 옷, 장갑까지 꼭 챙기세요!"

city = st.text_input("도시 이름을 입력하세요 (예: Seoul, London)")

if city:
    data = get_weather(city)
    if data:
        temp = data["main"]["temp"]
        weather_desc = data["weather"][0]["description"]
        st.write(f"현재 {city}의 기온: {temp}°C")
        st.write(f"날씨 상태: {weather_desc}")
        st.markdown(f"### 추천 옷차림:")
        st.write(recommend_clothes(temp, weather_desc))
    else:
        st.error("날씨 정보를 가져올 수 없습니다. 도시 이름을 확인해 주세요.")
else:
    st.info("도시 이름을 입력하면 날씨와 옷차림을 추천해 드립니다.")
