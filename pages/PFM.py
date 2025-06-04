import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# 세션 상태 초기화
if 'finance_data' not in st.session_state:
    st.session_state.finance_data = pd.DataFrame(columns=["Date", "Category", "Amount", "Type"])

# 파일 업로드 함수
def upload_file():
    uploaded_file = st.file_uploader("CSV 파일 업로드", type="csv")
    if uploaded_file is not None:
        data = pd.read_csv(uploaded_file)
        st.session_state.finance_data = data
        st.success("파일 업로드 완료!")
        st.write(st.session_state.finance_data.head())

# 카테고리별 지출 시각화 함수
def visualize_spending():
    # 지출 내역 필터링 (Type이 "Expense"인 것만)
    expense_data = st.session_state.finance_data[st.session_state.finance_data['Type'] == 'Expense']
    category_expense = expense_data.groupby('Category')['Amount'].sum().reset_index()

    # 시각화
    st.write("카테고리별 지출:")
    fig, ax = plt.subplots(figsize=(8, 5))
    ax.pie(category_expense['Amount'], labels=category_expense['Category'], autopct='%1.1f%%', startangle=90)
    ax.axis('equal')  # 원형으로 만듦
    st.pyplot(fig)

# 예산 관리
def budget_management():
    budget = st.number_input("월 예산 설정", min_value=0, step=1000)
    total_expense = st.session_state.finance_data[st.session_state.finance_data['Type'] == 'Expense']['Amount'].sum()

    remaining_budget = budget - total_expense
    st.write(f"총 지출: {total_expense}원")
    st.write(f"잔여 예산: {remaining_budget}원")

    if remaining_budget < 0:
        st.warning("예산을 초과했습니다!")

# 페이지 설정
st.title("개인 금융 관리 앱")
menu = ["파일 업로드", "카테고리별 지출 시각화", "예산 관리"]
choice = st.sidebar.selectbox("목록 선택", menu)

if choice == "파일 업로드":
    upload_file()
elif choice == "카테고리별 지출 시각화":
    if st.session_state.finance_data.shape[0] > 0:
        visualize_spending()
    else:
        st.warning("먼저 데이터를 업로드해주세요.")
elif choice == "예산 관리":
    if st.session_state.finance_data.shape[0] > 0:
        budget_management()
    else:
        st.warning("먼저 데이터를 업로드해주세요.")
