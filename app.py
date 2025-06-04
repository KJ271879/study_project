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
    st.experimental_rerun()

# 할 일 삭제
def delete_task(timeframe, index):
    st.session_state.todos[timeframe].pop(index)
    st.experimental_rerun()

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

# 일주일 페이지
elif choice == "일주일":
    st.header(f"이번 주 할 일 (Week {today.strftime('%U')})")
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

# 월별 페이지
elif choice == "월별":
    st.header(f"이번 달 할 일 (Month {today.month})")
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
