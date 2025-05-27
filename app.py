import streamlit as st

# 16가지 MBTI 유형과 간단 설명을 딕셔너리로 정의
mbti_descriptions = {
    "INTJ": "전략적인 계획가, 독립적이고 목표 지향적.",
    "INTP": "논리적인 사색가, 창의적이고 분석적.",
    "ENTJ": "대담한 리더, 결단력 있고 효율적.",
    "ENTP": "혁신적인 발명가, 토론을 즐기고 재치 있음.",
    "INFJ": "통찰력 있는 조언자, 이상주의자이자 헌신적.",
    "INFP": "이상적인 중재자, 내향적이고 가치 중심적.",
    "ENFJ": "카리스마 있는 지도자, 타인을 돕는 데 열정적.",
    "ENFP": "열정적인 활동가, 창의적이고 사람 중심적.",
    "ISTJ": "성실한 관리자, 책임감 있고 조직적.",
    "ISFJ": "헌신적인 수호자, 친절하고 신중함.",
    "ESTJ": "현실적인 관리자, 체계적이고 실용적.",
    "ESFJ": "사교적인 제공자, 타인에게 관심 많음.",
    "ISTP": "유능한 장인, 문제 해결에 능숙하고 실용적.",
    "ISFP": "조용한 예술가, 감성적이고 융통성 있음.",
    "ESTP": "모험적인 활동가, 즉흥적이고 에너지 넘침.",
    "ESFP": "사교적인 연예인, 즐거움과 현재에 집중."
}

st.title("MBTI 성격 유형 설명 앱")

# 사용자에게 MBTI 유형 선택하도록 라디오 버튼 제공
selected_mbti = st.radio("당신의 MBTI를 선택하세요:", list(mbti_descriptions.keys()))

# 선택한 MBTI 유형에 대한 설명 출력
st.write(f"### {selected_mbti} 성격 유형 설명")
st.write(mbti_descriptions[selected_mbti])
