import streamlit as st

st.title("주간 할 일 목록 앱")

# 요일 리스트
days = ["월요일", "화요일", "수요일", "목요일", "금요일", "토요일", "일요일"]

# 세션 상태 초기화
if "tasks" not in st.session_state:
    st.session_state.tasks = {day: [] for day in days}

# 함수 정의
def add_task(day, task_text):
    if task_text:
        st.session_state.tasks[day].append({"task": task_text, "done": False})

def toggle_done(day, idx):
    st.session_state.tasks[day][idx]["done"] = not st.session_state.tasks[day][idx]["done"]

def delete_task(day, idx):
    # 안전하게 새 리스트로 재구성
    st.session_state.tasks[day] = [
        task for i, task in enumerate(st.session_state.tasks[day]) if i != idx
    ]

# 요일별 인터페이스
for day in days:
    st.header(day)

    # 입력창과 버튼
    task_input = st.text_input(f"{day}에 추가할 할 일", key=f"input_{day}")
    if st.button(f"{day}에 추가", key=f"add_btn_{day}"):
        add_task(day, task_input)

    # 할 일 목록 출력
    for idx, task in enumerate(st.session_state.tasks[day]):
        col1, col2, col3 = st.columns([0.07, 0.75, 0.18])
        with col1:
            done = st.checkbox("", value=task["done"], key=f"{day}_done_{idx}")
            if done != task["done"]:
                toggle_done(day, idx)
        with col2:
            text = f"~~{task['task']}~~" if task["done"] else task["task"]
            st.markdown(text)
        with col3:
            if st.button("삭제", key=f"{day}_del_{idx}"):
                delete_task(day, idx)
                st.info(f"{task['task']} 항목이 삭제되었습니다.")
