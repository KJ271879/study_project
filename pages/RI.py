import streamlit as st
import pandas as pd
from geopy.geocoders import Nominatim

# 재활용 가능한 물품에 대한 정보 (간단한 예시)
recycling_info = {
    '플라스틱': '깨끗하게 세척 후 라벨 제거',
    '종이': '물에 젖지 않게 말린 후 배출',
    '유리병': '깨끗하게 세척 후 라벨 제거',
    '캔': '남은 내용물을 비운 후 배출',
    '옷': '기부 또는 헌옷 수거함에 배출'
}

# 재활용 센터 데이터 (예시)
recycling_centers = {
    '서울': {
        '주소': '서울특별시 강남구 테헤란로 100',
        '전화': '02-1234-5678',
        '운영시간': '월~금 09:00~18:00'
    },
    '부산': {
        '주소': '부산광역시 해운대구 센텀로 100',
        '전화': '051-9876-5432',
        '운영시간': '월~금 10:00~17:00'
    }
}

# 제목
st.title("재활용 정보 제공 앱")
st.markdown("이 앱은 재활용 가능한 물품에 대한 분리 배출 방법과, 지역별 재활용 센터 정보를 제공합니다.")

# 1. 재활용 가능한 물품 검색 기능
st.header("재활용 가능한 물품 검색")

item = st.text_input("물품명을 입력하세요 (예: 플라스틱, 종이, 유리병 등):")

if item:
    item = item.strip()  # 공백 제거
    if item in recycling_info:
        st.success(f"{item}에 대한 분리 배출 방법: {recycling_info[item]}")
    else:
        st.warning("해당 물품에 대한 정보가 없습니다. 다시 시도해 주세요.")

# 2. 지역별 재활용 센터 찾기
st.header("지역별 재활용 센터 찾기")

location = st.text_input("지역을 입력하세요 (예: 서울, 부산 등):")

if location:
    location = location.strip()
    if location in recycling_centers:
        st.success(f"{location} 지역의 재활용 센터 정보")
        st.write(f"**주소**: {recycling_centers[location]['주소']}")
        st.write(f"**전화**: {recycling_centers[location]['전화']}")
        st.write(f"**운영 시간**: {recycling_centers[location]['운영시간']}")
    else:
        st.warning(f"{location} 지역에 대한 정보가 없습니다. 다시 시도해 주세요.")

# 3. 사용자의 위치를 기반으로 재활용 센터 찾기
st.header("현재 위치 기반 재활용 센터 찾기")

geolocator = Nominatim(user_agent="recycling_locator")

user_location = st.text_input("현재 위치를 입력하세요 (예: 서울 강남구):")

if user_location:
    location = geolocator.geocode(user_location)
    if location:
        st.success(f"위치: {user_location} (위도: {location.latitude}, 경도: {location.longitude})")
        
        # 예시로 가까운 재활용 센터 검색 (여기서는 간단한 예시로 서울, 부산만 사용)
        if '서울' in user_location:
            st.write("가까운 재활용 센터: 서울 센터")
            st.write("주소: 서울특별시 강남구 테헤란로 100")
        elif '부산' in user_location:
            st.write("가까운 재활용 센터: 부산 센터")
            st.write("주소: 부산광역시 해운대구 센텀로 100")
        else:
            st.warning("위치 정보가 정확하지 않습니다. 다시 시도해 주세요.")
    else:
        st.warning("위치 정보가 올바르지 않습니다. 다시 입력해 주세요.")
