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
st.write("나타나는 숫자들 중 단 한 번의 선택으로 최고 숫자를 찾아보세요!")

# --- 설정 섹션 (사이드바) ---
with st.sidebar:
    st.header("⚙️ 게임 설정")
    
    # 1. 후보 수 선택 옵션 추가
    n_candidates = st.slider("후보 수 (n)", min_value=5, max_value=100, value=10, step=5)
    
    mode = st.radio("모드 선택", ["(1) 개별 실습", "(2) 전원 동일 실습"])
    
    room_key = ""
    if mode == "(2) 전원 동일 실습":
        room_key = st.text_input("방 코드 입력", "SAMU_2026")
    
    if st.button("🔄 게임 시작 / 초기화"):
        if mode == "(2) 전원 동일 실습":
            random.seed(f"{room_key}_{n_candidates}") # 방 코드와 n을 조합해 시드 생성
        else:
            random.seed(None)
            
        # 1~100 사이의 수 중 n개를 추출 (중복 없이)
        st.session_state.permutation = random.sample(range(1, 101), n_candidates)
        st.session_state.current_index = 0
        st.session_state.selected_candidate = None
        st.session_state.game_started = True

    # --- 만든 이 표기 (사이드바 하단) ---
        st.markdown("---")
        st.caption("created by 김사무@취미로배우는수학")

# --- 게임 진행 섹션 ---
if st.session_state.game_started:
    n = len(st.session_state.permutation)
    idx = st.session_state.current_index
    
    # 상단에 진행률 표시
    progress = (idx + 1) / n
    st.progress(progress)
    st.write(f"현재 후보: {idx + 1} / {n}")
    
    if st.session_state.selected_candidate is None and idx < n:
        current_val = st.session_state.permutation[idx]
        
        # 숫자 강조
        st.markdown(f"<h1 style='text-align: center; color: #FF4B4B; font-size: 100px;'>{current_val}</h1>", unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("👉 다음 후보 (Skip)", use_container_width=True):
                if idx < n - 1:
                    st.session_state.current_index += 1
                    st.rerun()
                else:
                    st.warning("마지막 후보입니다!")
        
        with col2:
            if st.button("✅ 선택 (Pick!)", use_container_width=True, type="primary"):
                st.session_state.selected_candidate = current_val
                st.rerun()
                
    # --- 결과 출력 ---
    elif st.session_state.selected_candidate is not None:
        max_val = max(st.session_state.permutation)
        st.success(f"당신의 선택: {st.session_state.selected_candidate}")
        st.info(f"이번 판의 최고 숫자: {max_val}")
        
        if st.session_state.selected_candidate == max_val:
            st.balloons()
            st.markdown("### 🎉 축하합니다! 1등을 찾으셨네요!")
        else:
            st.markdown(f"### 😅 아쉽습니다. 전체 {n}명 중 {st.session_state.permutation.index(max_val)+1}번째에 1등이 있었네요.")
            
        st.write("나타난 순서:", st.session_state.permutation)
        
    elif idx >= n:
        st.error("모든 후보를 보내버렸습니다. (선택 실패!)")
        st.write("전체 순서:", st.session_state.permutation)

else:
    st.info("왼쪽 사이드바에서 설정을 완료한 후 '게임 시작' 버튼을 눌러주세요.")

# --- 만든 이 표기 (메인 화면 하단) ---
st.markdown("---")
st.markdown("<div style='text-align: right; color: gray; font-size: 0.8em;'>created by 김사무@취미로배우는수학</div>", unsafe_allow_html=True)
