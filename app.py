import streamlit as st

st.title("주간 할 일 목록 앱")

# 일주일 날짜 리스트 (월~일)
days = ["월요일", "화요일", "수요일", "목요일", "금요일", "토요일", "일요일"]

# 세션 상태에 할 일 데이터 저장용 초기화
if "tasks" not in st.session_state:
    st.session_state.tasks = {day: [] for day in days}

# 입력창 초기화를 위한 세션 상태 추가
for day in days:
    if f"input_{day}" not in st.session_state:
        st.session_state[f"input_{day}"] = ""

def add_task(day, task):
    if task:
        st.session_state.tasks[day].append({"task": task, "done": False})

def toggle_done(day, idx):
    st.session_state.tasks[day][idx]["done"] = not st.session_state.tasks[day][idx]["done"]

def delete_task(day, idx):
    st.session_state.tasks[day].pop(idx)

# 요일별로 할 일 입력 및 목록 출력
for day in days:
    st.header(day)
    with st.expander(f"{day} 할 일 추가"):
        new_task = st.text_input(f"{day}에 추가할 할 일", key=f"input_{day}")
        if st.button("추가", key=f"add_{day}"):
            add_task(day, new_task)
            st.session_state[f"input_{day}"] = ""  # 입력창 초기화

    # 기존 할 일 목록 보여주기
    tasks = st.session_state.tasks[day]
    for i, task_data in enumerate(tasks):
        col1, col2, col3 = st.columns([0.05, 0.8, 0.15])
        with col1:
            checked = st.checkbox("", value=task_data["done"], key=f"done_{day}_{i}")
            if checked != task_data["done"]:
                toggle_done(day, i)
        with col2:
            if task_data["done"]:
                st.markdown(f"~~{task_data['task']}~~")
            else:
                st.markdown(task_data['task'])
        with col3:
            if st.button("삭제", key=f"del_{day}_{i}"):
                delete_task(day, i)
