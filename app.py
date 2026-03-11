import streamlit as st
import random

# --- 앱 설정 ---
st.set_page_config(page_title="Secretary Game: Optimal Stopping", layout="centered")

# --- 세션 상태 초기화 ---
if 'game_started' not in st.session_state:
    st.session_state.game_started = False
if 'current_index' not in st.session_state:
    st.session_state.current_index = 0
if 'selected_candidate' not in st.session_state:
    st.session_state.selected_candidate = None
if 'permutation' not in st.session_state:
    st.session_state.permutation = []

# --- 제목 및 설명 ---
st.title("🏹 비서 게임: 최적 정지 실습")
st.write("1부터 50 사이의 숫자 10개가 무작위 순서로 나타납니다. 단 한 번의 선택 기회로 최고 숫자를 찾아보세요!")

# --- 설정 섹션 ---
with st.sidebar:
    st.header("⚙️ 게임 설정")
    mode = st.radio("모드 선택", ["(1) 개별 실습", "(2) 전원 동일 실습"])
    
    room_key = ""
    if mode == "(2) 전원 동일 실습":
        room_key = st.text_input("방 코드 입력 (강연자가 안내한 코드)", "SAMU_2026")
    
    if st.button("🔄 게임 시작 / 초기화"):
        # 초기화 로직
        if mode == "(2) 전원 동일 실습":
            random.seed(room_key) # 방 코드를 시드로 사용해 순열 동기화
        else:
            random.seed(None) # 완전 랜덤
            
        st.session_state.permutation = random.sample(range(1, 51), 10)
        st.session_state.current_index = 0
        st.session_state.selected_candidate = None
        st.session_state.game_started = True

# --- 게임 진행 섹션 ---
if st.session_state.game_started:
    n = len(st.session_state.permutation)
    idx = st.session_state.current_index
    
    if st.session_state.selected_candidate is None and idx < n:
        st.subheader(f"후보 {idx + 1} / {n}")
        current_val = st.session_state.permutation[idx]
        
        # 큰 숫자로 표시
        st.markdown(f"<h1 style='text-align: center; color: #FF4B4B;'>{current_val}</h1>", unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("👉 다음 후보 보기"):
                if idx < n - 1:
                    st.session_state.current_index += 1
                    st.rerun()
                else:
                    st.warning("마지막 후보입니다! 선택하거나 게임을 종료하세요.")
        
        with col2:
            if st.button("✅ 이 사람을 선택!"):
                st.session_state.selected_candidate = current_val
                st.rerun()
                
    # --- 결과 출력 ---
    elif st.session_state.selected_candidate is not None:
        max_val = max(st.session_state.permutation)
        st.success(f"당신의 선택: {st.session_state.selected_candidate}")
        st.info(f"전체 후보 중 최고 숫자: {max_val}")
        
        if st.session_state.selected_candidate == max_val:
            st.balloons()
            st.write("🎉 축하합니다! 최고의 비서를 찾으셨네요!")
        else:
            st.write("😅 아쉽습니다. 1등을 놓쳤네요.")
            
        # 전체 순열 공개
        st.write("전체 순서:", st.session_state.permutation)
        
    elif idx >= n:
        st.error("아무도 선택하지 못한 채 모든 후보가 지나갔습니다. (파산!)")
        st.write("전체 순서:", st.session_state.permutation)

else:
    st.info("왼쪽 사이드바에서 설정을 완료한 후 '게임 시작' 버튼을 눌러주세요.")
