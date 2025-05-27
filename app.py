import streamlit as st

st.title("주간 할 일 목록 앱")

# 요일 리스트
days = ["월요일", "화요일", "수요일", "목요일", "금요일", "토요일", "일요일"]

# 세션 상태 초기화
if "tasks" not in st.session_state:
    st.session_state.tasks = {day: [] for day in days}

def add_task(day, task):
    if task:
        st.session_state.tasks[day].append({"task": task, "done": False})

def toggle_done(day, idx):
    st.session_state.tasks[day][idx]["done"] = not st.session_state.tasks[day][idx]["done"]

def delete_task(day, idx):
    st.session_state.tasks[day].pop(idx)

# 요일별 할 일 관리
for day in days:
    st.header(day)

    with st.expander(f"{day} 할 일 추가"):
        input_key = f"input_{day}"
        new_task = st.text_input(f"{day}에 추가할 할 일", key=input_key)
        if st.button(f"{day} 추가", key=f"add_btn_{day}"):
            add_task(day, new_task)
            # rerun으로 입력창 초기화
            st.experimental_rerun()

    # 할 일 목록 출력
    tasks = st.session_state.tasks[day]
    for i, task in enumerate(tasks):
        col1, col2, col3 = st.columns([0.05, 0.8, 0.15])
        with col1:
            done = st.checkbox("", value=task["done"], key=f"{day}_done_{i}")
            if done != task["done"]:
                toggle_done(day, i)
                st.experimental_rerun()
        with col2:
            if task["done"]:
                st.markdown(f"~~{task['task']}~~")
            else:
                st.markdown(task["task"])
        with col3:
            if st.button("삭제", key=f"{day}_del_{i}"):
                delete_task(day, i)
                st.experimental_rerun()
