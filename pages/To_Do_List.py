import streamlit as st
import datetime

# 오늘 날짜
today = datetime.date.today()

# 세션 상태 초기화
if 'todos' not in st.session_state:
    st.session_state.todos = {
        'day': [],
        'week': [],
        'month': []
    }

# 할 일 추가
def add_task(timeframe):
    task = st.text_input(f"할 일 추가 ({timeframe})", "")
    if st.button(f"{timeframe} 할 일 추가"):
        if task:
            st.session_state.todos[timeframe].append({'task': task, 'completed': False})
            st.success(f"{timeframe} 할 일이 추가되었습니다!")
        else:
            st.warning("할 일을 입력해 주세요.")

# 할 일 완료 체크
def complete_task(timeframe, index):
    st.session_state.todos[timeframe][index]['completed'] = True

# 할 일 삭제
def delete_task(timeframe, index):
    # 해당 항목 삭제
    del st.session_state.todos[timeframe][index]

# 주차 기간 계산
def get_week_period(date):
    start_date = date - datetime.timedelta(days=date.weekday())  # 주 시작일 (월요일)
    end_date = start_date + datetime.timedelta(days=6)  # 주 종료일 (일요일)
    return start_date, end_date

# 월별 기간 계산
def get_month_period(date):
    start_date = date.replace(day=1)  # 이번 달 1일
    # 다음 달 1일을 구하고, 하루를 빼면 이번 달 마지막 날이 나옵니다.
    next_month = start_date.replace(day=28) + datetime.timedelta(days=4)
    end_date = next_month - datetime.timedelta(days=next_month.day)
    return start_date, end_date

# 메인 페이지
st.title("To-Do 리스트")
menu = ["하루", "일주일", "월별"]
choice = st.sidebar.selectbox("목록 선택", menu)

# 하루 페이지
if choice == "하루":
    st.header(f"오늘 할 일 ({today})")
    add_task("day")
    for i, todo in enumerate(st.session_state.todos['day']):
        col1, col2, col3 = st.columns([6, 1, 1])
        with col1:
            checkbox = st.checkbox(todo['task'], value=todo['completed'], key=f'day_{i}')
            if checkbox and not todo['completed']:
                complete_task("day", i)
        with col2:
            if todo['completed']:
                st.text('완료됨')
        with col3:
            if st.button(f"삭제", key=f'day_delete_{i}'):
                delete_task("day", i)
                # 삭제 후, 페이지 새로 고침을 위해 상태 업데이트
                st.experimental_rerun()  # 삭제 후 페이지 새로 고침

# 일주일 페이지
elif choice == "일주일":
    start_date, end_date = get_week_period(today)
    st.header(f"이번 주 할 일 ({start_date} ~ {end_date})")
    add_task("week")
    for i, todo in enumerate(st.session_state.todos['week']):
        col1, col2, col3 = st.columns([6, 1, 1])
        with col1:
            checkbox = st.checkbox(todo['task'], value=todo['completed'], key=f'week_{i}')
            if checkbox and not todo['completed']:
                complete_task("week", i)
        with col2:
            if todo['completed']:
                st.text('완료됨')
        with col3:
            if st.button(f"삭제", key=f'week_delete_{i}'):
                delete_task("week", i)
                st.experimental_rerun()  # 삭제 후 페이지 새로 고침

# 월별 페이지
elif choice == "월별":
    start_date, end_date = get_month_period(today)
    st.header(f"이번 달 할 일 ({start_date} ~ {end_date})")
    add_task("month")
    for i, todo in enumerate(st.session_state.todos['month']):
        col1, col2, col3 = st.columns([6, 1, 1])
        with col1:
            checkbox = st.checkbox(todo['task'], value=todo['completed'], key=f'month_{i}')
            if checkbox and not todo['completed']:
                complete_task("month", i)
        with col2:
            if todo['completed']:
                st.text('완료됨')
        with col3:
            if st.button(f"삭제", key=f'month_delete_{i}'):
                delete_task("month", i)
                st.experimental_rerun()  # 삭제 후 페이지 새로 고침
