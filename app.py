import streamlit as st
import datetime

# 할 일 목록을 저장하는 전역 딕셔너리
todos = {
    'day': [],
    'week': [],
    'month': []
}

# 함수: 할 일 추가
def add_task(timeframe):
    task = st.text_input(f"할 일 추가 ({timeframe})", "")
    if st.button(f"{timeframe} 할 일 추가"):
        if task:
            todos[timeframe].append({'task': task, 'completed': False})
            st.success(f"{timeframe} 할 일이 추가되었습니다!")
        else:
            st.warning("할 일을 입력해 주세요.")

# 함수: 할 일 완료 체크
def complete_task(timeframe, index):
    todos[timeframe][index]['completed'] = True

# 함수: 할 일 삭제
def delete_task(timeframe, index):
    todos[timeframe].pop(index)

# 메인 페이지
st.title("To-Do 리스트")
menu = ["하루", "일주일", "월별"]
choice = st.sidebar.selectbox("목록 선택", menu)

# 오늘 날짜
today = datetime.date.today()

# 하루 페이지
if choice == "하루":
    st.header(f"오늘 할 일 ({today})")
    add_task("day")
    for i, todo in enumerate(todos['day']):
        col1, col2, col3 = st.columns([6, 1, 1])
        with col1:
            st.checkbox(todo['task'], value=todo['completed'], key=f'day_{i}', on_change=complete_task, args=('day', i))
        with col2:
            if todo['completed']:
                st.text('완료됨')
        with col3:
            if st.button(f"삭제", key=f'day_delete_{i}'):
                delete_task("day", i)
                st.experimental_rerun()

# 일주일 페이지
elif choice == "일주일":
    st.header(f"이번 주 할 일 (Week {today.strftime('%U')})")
    add_task("week")
    for i, todo in enumerate(todos['week']):
        col1, col2, col3 = st.columns([6, 1, 1])
        with col1:
            st.checkbox(todo['task'], value=todo['completed'], key=f'week_{i}', on_change=complete_task, args=('week', i))
        with col2:
            if todo['completed']:
                st.text('완료됨')
        with col3:
            if st.button(f"삭제", key=f'week_delete_{i}'):
                delete_task("week", i)
                st.experimental_rerun()

# 월별 페이지
elif choice == "월별":
    st.header(f"이번 달 할 일 (Month {today.month})")
    add_task("month")
    for i, todo in enumerate(todos['month']):
        col1, col2, col3 = st.columns([6, 1, 1])
        with col1:
            st.checkbox(todo['task'], value=todo['completed'], key=f'month_{i}', on_change=complete_task, args=('month', i))
        with col2:
            if todo['completed']:
                st.text('완료됨')
        with col3:
            if st.button(f"삭제", key=f'month_delete_{i}'):
                delete_task("month", i)
                st.experimental_rerun()
