import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import io

# --- 기본 설정 및 데이터 초기화 ---
st.set_page_config(layout="wide", page_title="나만의 가계부")
st.title("💰 나만의 똑똑한 가계부")
st.markdown("수입과 지출을 손쉽게 관리하고 재정 상태를 한눈에 파악하세요!")

# 세션 상태에 DataFrame 초기화 (앱이 새로고침되어도 데이터 유지)
if "df" not in st.session_state:
    st.session_state.df = pd.DataFrame(columns=["날짜", "종류", "금액", "메모"])

# --- 입력 폼 ---
st.sidebar.header("💸 새 기록 추가")
with st.sidebar.form("entry_form", clear_on_submit=True):
    date = st.date_input("날짜", value=pd.to_datetime("today"))
    kind = st.selectbox("종류", ["수입", "지출"])
    amount = st.number_input("금액 (원)", min_value=0, step=1000, format="%d")
    memo = st.text_input("메모 (선택 사항)")
    
    submitted = st.form_submit_button("✅ 기록 추가하기")

    if submitted:
        if amount == 0:
            st.error("금액은 0보다 커야 합니다.")
        else:
            # 새 항목을 DataFrame에 추가
            new_entry = {"날짜": date, "종류": kind, "금액": amount, "메모": memo}
            st.session_state.df = pd.concat([st.session_state.df, pd.DataFrame([new_entry])], ignore_index=True)
            st.success("🎉 새로운 기록이 성공적으로 추가되었습니다!")

# --- 데이터 표시 및 요약 ---
df = st.session_state.df.copy() # 원본 데이터프레임 보호를 위해 복사본 사용

if not df.empty:
    # 날짜 기준으로 정렬
    df = df.sort_values(by="날짜", ascending=False).reset_index(drop=True)

    st.subheader("📊 모든 가계부 내역")
    # DataFrame 표시 (인덱스 제거)
    st.dataframe(df.style.format({"금액": "{:,.0f} 원"}), use_container_width=True, hide_index=True)

    # --- 총 합계 계산 ---
    st.markdown("---")
    col1, col2, col3 = st.columns(3)
    
    income_sum = df.loc[df["종류"] == "수입", "금액"].sum()
    expense_sum = df.loc[df["종류"] == "지출", "금액"].sum()
    balance = income_sum - expense_sum

    with col1:
        st.metric("총 수입", f"{income_sum:,.0f} 원", delta_color="off")
    with col2:
        st.metric("총 지출", f"{expense_sum:,.0f} 원", delta_color="off")
    with col3:
        # 잔액에 따라 색상 변경
        if balance >= 0:
            st.metric("현재 잔액", f"{balance:,.0f} 원", delta_color="normal")
        else:
            st.metric("현재 잔액", f"{balance:,.0f} 원", delta_color="inverse")

    # --- 시각화 ---
    st.markdown("---")
    st.subheader("📈 날짜별 수입 및 지출 추이")

    # Matplotlib 한글 폰트 설정
    plt.rcParams['font.family'] = 'Malgun Gothic' # Windows 사용자
    # plt.rcParams['font.family'] = 'AppleGothic' # Mac 사용자
    plt.rcParams['axes.unicode_minus'] = False # 마이너스 폰트 깨짐 방지

    # 날짜별 수입/지출 집계
    pivot_df = df.pivot_table(index="날짜", columns="종류", values="금액", aggfunc='sum', fill_value=0).reset_index()
    pivot_df["날짜"] = pd.to_datetime(pivot_df["날짜"])

    fig, ax = plt.subplots(figsize=(12, 6))
    width = 0.35  # 바 너비

    # 날짜 offset을 사용하여 바 겹치지 않게 하기
    x = pivot_df["날짜"]

    # 수입 바 그리기 (수입 데이터가 있을 경우)
    if '수입' in pivot_df.columns:
        ax.bar(x - pd.Timedelta(days=width/2), pivot_df["수입"], width=width, label="수입", color="#28a745") # Bootstrap green
    
    # 지출 바 그리기 (지출 데이터가 있을 경우)
    if '지출' in pivot_df.columns:
        ax.bar(x + pd.Timedelta(days=width/2), pivot_df["지출"], width=width, label="지출", color="#dc3545") # Bootstrap red

    ax.set_xlabel("날짜", fontsize=12)
    ax.set_ylabel("금액 (원)", fontsize=12)
    ax.set_title("날짜별 수입 및 지출", fontsize=16)
    ax.legend(fontsize=10)
    fig.autofmt_xdate(rotation=45) # x축 라벨 회전

    ax.grid(axis='y', linestyle='--', alpha=0.7) # y축 그리드 추가

    st.pyplot(fig)
    
    # --- 데이터 내보내기 ---
    st.markdown("---")
    st.subheader("📥 데이터 내보내기")
    
    csv_buffer = io.StringIO()
    df.to_csv(csv_buffer, index=False, encoding='utf-8-sig') # 한글 깨짐 방지를 위해 'utf-8-sig' 사용
    st.download_button(
        label="CSV 파일로 다운로드",
        data=csv_buffer.getvalue(),
        file_name="가계부_내역.csv",
        mime="text/csv",
        key="download_csv_button"
    )

    st.markdown("---")

else:
    st.info("아직 가계부 내역이 없습니다. 왼쪽 사이드바에서 기록을 추가해보세요! 🚀")

st.markdown("---")
st.info("© 2024 나만의 가계부. 궁금한 점이 있으신가요?")
