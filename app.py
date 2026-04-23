import json
import random
import base64
import html
from pathlib import Path

import streamlit as st

# -----------------------------
# 기본 설정
# -----------------------------
st.set_page_config(
    page_title="세계 수도 챌린지",
    page_icon="🌍",
    layout="wide",
    initial_sidebar_state="expanded",
)

BASE_DIR = Path(__file__).parent
DATA_PATH = BASE_DIR / "data" / "capitals_quiz.json"
FLAG_DIR = BASE_DIR / "assets" / "flags"
HEADER_IMAGE_PATH = BASE_DIR / "assets" / "header-map.jpg"
USERS_PATH = BASE_DIR / "data" / "users.json"

APP_TITLE = "세계 수도 챌린지"
STUDENT_ID = "2023204017"
STUDENT_NAME = "최유진"


# -----------------------------
# 파일 확장자 탐색 함수
# -----------------------------

SUPPORTED_FLAG_EXTENSIONS = [".gif", ".png", ".bmp", ".jpg", ".jpeg"]

def find_flag_path(iso2: str) -> Path | None:
    for ext in SUPPORTED_FLAG_EXTENSIONS:
        candidate = FLAG_DIR / f"{iso2.upper()}{ext}"
        if candidate.exists():
            return candidate
    return None

def render_flag_image(iso2: str, caption: str):
    flag_path = find_flag_path(iso2)

    if flag_path is None:
        st.warning(f"{iso2.upper()} 국기 파일을 찾을 수 없습니다.")
        return

    mime_map = {
        ".gif": "image/gif",
        ".png": "image/png",
        ".bmp": "image/bmp",
        ".jpg": "image/jpeg",
        ".jpeg": "image/jpeg",
    }

    mime_type = mime_map.get(flag_path.suffix.lower(), "image/png")
    image_bytes = flag_path.read_bytes()
    encoded = base64.b64encode(image_bytes).decode("utf-8")
    safe_caption = html.escape(caption)

    st.markdown(
        f"""
        <div style="text-align:center;">
            <img
                src="data:{mime_type};base64,{encoded}"
                style="
                    width:100%;
                    max-width:260px;
                    border-radius:12px;
                    border:1px solid #e5e7eb;
                    box-shadow:0 4px 12px rgba(0,0,0,0.08);
                "
            />
            <p style="margin-top:0.6rem; color:#6b7280; font-size:0.95rem;">
                {safe_caption}
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )


def image_to_base64(image_path: Path) -> str:
    image_bytes = image_path.read_bytes()
    return base64.b64encode(image_bytes).decode("utf-8")

# -----------------------------
# 스타일
# -----------------------------
st.markdown(
    """
    <style>
    .hero-card {
        padding: 1.2rem 1.4rem;
        border-radius: 18px;
        background: linear-gradient(135deg, #e0f2fe, #f0fdf4);
        border: 1px solid #dbeafe;
        margin-bottom: 1rem;
    }

    .meta-card {
        padding: 1rem 1.2rem;
        border-radius: 16px;
        background-color: #f8fafc;
        border: 1px solid #e2e8f0;
        text-align: center;
    }

    .feedback-success {
        padding: 1rem 1.2rem;
        border-radius: 16px;
        background: #ecfdf5;
        border: 1px solid #10b981;
        color: #065f46;
        font-weight: 600;
        margin-top: 1rem;
        margin-bottom: 1rem;
    }

    .feedback-error {
        padding: 1rem 1.2rem;
        border-radius: 16px;
        background: #fef2f2;
        border: 1px solid #ef4444;
        color: #991b1b;
        font-weight: 600;
        margin-top: 1rem;
        margin-bottom: 1rem;
    }

    .grade-card {
        padding: 1.2rem 1.4rem;
        border-radius: 18px;
        background: #f8fafc;
        border: 1px solid #cbd5e1;
        margin-top: 1rem;
        margin-bottom: 1rem;
    }

    /* -----------------------------
       Sidebar
    ----------------------------- */
    section[data-testid="stSidebar"] {
        background-color: #f3f4f8;
        border-right: 1px solid #e6e8ef;
    }

    section[data-testid="stSidebar"] .block-container {
        min-height: 100vh;
        display: flex;
        flex-direction: column;
        padding: 2.4rem 1rem 2rem 1rem;
    }

    .sidebar-top-row {
        display: flex;
        align-items: center;
        margin-bottom: 1.8rem;
    }

    .sidebar-menu-title {
        font-size: 1.65rem;
        font-weight: 800;
        color: #2f3442;
        display: flex;
        align-items: center;
        gap: 0.4rem;
    }

    .sidebar-welcome-box {
        background: #dfe6df;
        color: #4f8a55;
        border-radius: 14px;
        padding: 0.95rem 1rem;
        font-size: 0.94rem;
        font-weight: 700;
        margin-bottom: 1rem;
    }

    .sidebar-info-card {
        background: #dbe4f5;
        border-radius: 18px;
        padding: 1.9rem 1rem 1rem 1rem;
        text-align: center;
        margin-bottom: 1rem;
    }

    .sidebar-student-id {
        color: #3466b9;
        font-size: 1rem;
        font-weight: 800;
        line-height: 1.35;
    }

    .sidebar-student-name {
        color: #3466b9;
        font-size: 1rem;
        font-weight: 800;
        margin-top: 0.2rem;
    }

    .sidebar-info-label {
        color: #3466b9;
        font-size: 1rem;
        font-weight: 700;
        text-align: left;
        margin-top: 1.2rem;
        padding-left: 0.2rem;
    }

    .sidebar-bottom-spacer {
        height: 1;
    }

    section[data-testid="stSidebar"] .block-container > div:has(.sidebar-bottom-spacer) {
        flex-grow: 1;
    }

    /* 사이드바 버튼 공통 스타일 */
    section[data-testid="stSidebar"] .stButton {
        display: flex;
        justify-content: center;
    }

    section[data-testid="stSidebar"] .stButton > button {
        background: transparent !important;
        border: none !important;
        box-shadow: none !important;
        padding: 0 !important;
        min-height: auto !important;
        width: auto !important;
        font-size: 1.05rem !important;
        font-weight: 500 !important;
        line-height: 1.5 !important;
    }

    section[data-testid="stSidebar"] .stButton > button:hover,
    section[data-testid="stSidebar"] .stButton > button:focus {
        background: transparent !important;
        color: #ff7d7d !important;
        border: none !important;
        box-shadow: none !important;
    }

    /* 첫 번째 버튼 = 캐시 초기화 */
    section[data-testid="stSidebar"] .stButton:nth-last-of-type(2) > button {
        color: #ff7d7d !important;
        margin-bottom: 0.9rem;
    }

    /* 마지막 버튼 = 로그아웃 */
    section[data-testid="stSidebar"] .stButton:last-of-type > button {
        color: #3b3f4a !important;
    }

    .app-header {
    position: relative;
    overflow: hidden;
    border-radius: 24px;
    padding: 3rem 2.5rem;
    margin-bottom: 1.5rem;
    color: white;
    background-size: cover;
    background-position: center;
    box-shadow: 0 12px 28px rgba(15, 23, 42, 0.18);
}

.app-header::before {
    content: "";
    position: absolute;
    inset: 0;
    background: rgba(15, 23, 42, 0.52);
    z-index: 0;
}

.app-header-content {
    position: relative;
    z-index: 1;
}

.app-header-title {
    font-size: 2.5rem;
    font-weight: 800;
    margin-bottom: 1rem;
    letter-spacing: -0.03em;
}

.app-header-description {
    font-size: 1.08rem;
    font-weight: 500;
    line-height: 1.7;
    max-width: 620px;
}
    </style>
    """,
    unsafe_allow_html=True,
)


# -----------------------------
# 유틸 함수
# -----------------------------
@st.cache_data(show_spinner="퀴즈 데이터를 불러오는 중입니다...")
def load_users():
    with open(USERS_PATH, "r", encoding="utf-8") as f:
        return json.load(f)
    
def load_quiz_data():
    with open(DATA_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


def normalize_text(text: str) -> str:
    return (
        text.strip()
        .lower()
        .replace(" ", "")
        .replace(".", "")
        .replace(",", "")
        .replace("'", "")
    )


def is_correct_answer(user_answer: str, item: dict) -> bool:
    normalized_user_answer = normalize_text(user_answer)
    accepted_answers = [item["capital"]] + item.get("aliases", [])
    normalized_answers = [normalize_text(answer) for answer in accepted_answers]
    return normalized_user_answer in normalized_answers


def get_grade(score: int, total: int):
    ratio = score / total if total else 0

    if ratio >= 0.8:
        return "수도 마스터", "훌륭해요! 세계 주요 수도를 매우 잘 알고 있어요."
    elif ratio >= 0.5:
        return "지리 탐험가", "좋아요! 기본적인 수도 지식이 잘 잡혀 있어요."
    return "여행 초보", "아직은 연습이 더 필요해요. 다시 도전해봐요!"


def init_session_state():
    defaults = {
        "logged_in": False,
        "username": "",
        "quiz_started": False,
        "quiz_finished": False,
        "current_index": 0,
        "score": 0,
        "selected_continent": "아시아",
        "quiz_questions": [],
        "results": [],
        "feedback": None,
    }

    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value


def reset_quiz_state():
    st.session_state.quiz_started = False
    st.session_state.quiz_finished = False
    st.session_state.current_index = 0
    st.session_state.score = 0
    st.session_state.quiz_questions = []
    st.session_state.results = []
    st.session_state.feedback = None


def logout():
    st.session_state.logged_in = False
    st.session_state.username = ""
    reset_quiz_state()


def start_quiz(all_questions):
    QUIZ_COUNT = 10
    selected = [
        q for q in all_questions if q["continent"] == st.session_state.selected_continent
    ]
    random.shuffle(selected)
    st.session_state.quiz_questions = selected[:QUIZ_COUNT]
    st.session_state.quiz_started = True
    st.session_state.quiz_finished = False
    st.session_state.current_index = 0
    st.session_state.score = 0
    st.session_state.results = []
    st.session_state.feedback = None


def go_next():
    st.session_state.current_index += 1
    st.session_state.feedback = None

    if st.session_state.current_index >= len(st.session_state.quiz_questions):
        st.session_state.quiz_finished = True


# -----------------------------
# 초기화
# -----------------------------
init_session_state()
quiz_data = load_quiz_data()
valid_users = load_users()

# -----------------------------
# 사이드바
# -----------------------------
st.sidebar.markdown(
    """
    <div class="sidebar-top-row">
        <div class="sidebar-menu-title">🌍 Welcome!</div>
    </div>
    """,
    unsafe_allow_html=True,
)

if st.session_state.logged_in:
    st.sidebar.markdown(
        f'<div class="sidebar-welcome-box">{st.session_state.username} 님, 환영합니다!</div>',
        unsafe_allow_html=True,
    )

    st.sidebar.markdown(
        f"""
        <div class="sidebar-info-card">
            <div class="sidebar-student-id">{STUDENT_ID}</div>
            <div class="sidebar-student-name">{STUDENT_NAME}</div>
            <div class="sidebar-info-label">Info</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.sidebar.markdown('<div class="sidebar-bottom-spacer"></div>', unsafe_allow_html=True)

    if st.sidebar.button("캐시 초기화", key="sidebar_clear_cache"):
        load_quiz_data.clear()
        st.rerun()

    if st.sidebar.button("로그아웃", key="sidebar_logout"):
        logout()
        st.rerun()
else:
    st.sidebar.caption("로그인 후 퀴즈를 시작할 수 있습니다.")
    st.sidebar.markdown(
        f"""
        <div class="sidebar-info-card">
            <div class="sidebar-student-id">{STUDENT_ID}</div>
            <div class="sidebar-student-name">{STUDENT_NAME}</div>
            <div class="sidebar-info-label">Info</div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    

# -----------------------------
# 첫 화면 공통 헤더
# -----------------------------
header_image_base64 = image_to_base64(HEADER_IMAGE_PATH)

st.markdown(
    f"""
    <div
        class="app-header"
        style="background-image: url('data:image/jpeg;base64,{header_image_base64}');"
    >
        <div class="app-header-content">
            <div class="app-header-title">{APP_TITLE}</div>
            <div class="app-header-description">
                나라와 국기를 보고 수도를 맞히는 단답형 퀴즈입니다.<br>
                대륙별로 문제를 풀고, 최종 등급까지 확인해보세요.
            </div>
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

st.divider()


# -----------------------------
# 로그인 화면
# -----------------------------
if not st.session_state.logged_in:
    st.subheader("Login")

    with st.form("login_form"):
        user_id = st.text_input("아이디")
        password = st.text_input("비밀번호", type="password")
        login_submitted = st.form_submit_button("로그인")

        if login_submitted:
            if valid_users.get(user_id) == password:
                st.session_state.logged_in = True
                st.session_state.username = user_id
                st.success("로그인에 성공했습니다!")
                st.rerun()
            else:
                st.error("아이디 또는 비밀번호가 올바르지 않습니다.")

    st.stop()


# -----------------------------
# 퀴즈 시작 전 화면
# -----------------------------
if not st.session_state.quiz_started and not st.session_state.quiz_finished:
    st.subheader("퀴즈 설정")

    st.write("총 **10문제 단답형** 구성입니다.")

    st.session_state.selected_continent = st.selectbox(
        "대륙을 선택해 주세요",
        ["아시아", "유럽", "아프리카", "아메리카"],
        index=["아시아", "유럽", "아프리카", "아메리카"].index(
            st.session_state.selected_continent
        ),
    )

    st.write("")

    if st.button("퀴즈 시작하기", type="primary"):
        start_quiz(quiz_data)
        st.rerun()

    st.stop()


# -----------------------------
# 결과 화면
# -----------------------------
if st.session_state.quiz_finished:
    total = len(st.session_state.quiz_questions)
    score = st.session_state.score
    grade, message = get_grade(score, total)

    st.header("🏁 퀴즈 결과")
    st.metric("최종 점수", f"{score} / {total}")

    st.markdown(
        f"""
        <div class="grade-card">
            <h3>최종 등급: {grade}</h3>
            <p>{message}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    if grade == "수도 마스터":
        st.balloons()

    with st.expander("문제별 결과 보기", expanded=True):
        for idx, result in enumerate(st.session_state.results, start=1):
            status = "✅ 정답" if result["correct"] else "❌ 오답"
            st.write(
                f"{idx}. {result['country']} | 내 답: {result['user_answer']} | "
                f"정답: {result['correct_answer']} | {status}"
            )

    left_spacer, col1, col2, right_spacer = st.columns([3, 1, 1, 3], gap="small")

    with col1:
        if st.button("같은 대륙 다시 풀기"):
            start_quiz(quiz_data)
            st.rerun()

    with col2:
        if st.button("처음으로 돌아가기"):
            reset_quiz_state()
            st.rerun()

    st.stop()


# -----------------------------
# 퀴즈 진행 화면
# -----------------------------
question = st.session_state.quiz_questions[st.session_state.current_index]
total_questions = len(st.session_state.quiz_questions)
current_no = st.session_state.current_index + 1

st.header(f"문제 {current_no} / {total_questions}")
st.progress(current_no / total_questions)

left_col, right_col = st.columns([1, 2])

with left_col:
    render_flag_image(question["iso2"], f"{question['country']}")

with right_col:
    st.subheader(f"{question['country']}의 수도는 어디일까요?")
    st.caption("정답을 한글 또는 영문으로 입력해도 됩니다.")

    if st.session_state.feedback is None:
        with st.form(f"quiz_form_{st.session_state.current_index}"):
            user_answer = st.text_input("수도를 입력하세요")
            submitted = st.form_submit_button("정답 제출")

            if submitted:
                if not user_answer.strip():
                    st.warning("답을 입력해주세요.")
                else:
                    correct = is_correct_answer(user_answer, question)

                    if correct:
                        st.session_state.score += 1
                        st.session_state.feedback = {
                            "correct": True,
                            "message": f"정답입니다! {question['country']}의 수도는 {question['capital']}입니다. 🎉",
                        }
                        st.toast("정답입니다! 🎉")
                    else:
                        st.session_state.feedback = {
                            "correct": False,
                            "message": f"오답입니다. 정답은 {question['capital']}입니다.",
                        }
                        st.toast("아쉬워요! 다음 문제에서 만회해봐요.")

                    st.session_state.results.append(
                        {
                            "country": question["country"],
                            "user_answer": user_answer,
                            "correct_answer": question["capital"],
                            "correct": correct,
                        }
                    )
                    st.rerun()

    else:
        if st.session_state.feedback["correct"]:
            st.markdown(
                f"""
                <div class="feedback-success">
                    {st.session_state.feedback["message"]}
                </div>
                """,
                unsafe_allow_html=True,
            )
            st.success("계속해서 다음 문제에 도전해보세요!")
        else:
            st.markdown(
                f"""
                <div class="feedback-error">
                    {st.session_state.feedback["message"]}
                </div>
                """,
                unsafe_allow_html=True,
            )
            st.error("괜찮아요. 다음 문제를 맞혀봐요!")

        next_label = "결과 보기" if current_no == total_questions else "다음 문제"
        if st.button(next_label, type="primary"):
            go_next()
            st.rerun()