import streamlit as st
import streamlit.components.v1 as components
import random

# පිටුවේ සැකසුම්
st.set_page_config(page_title="වතුර භාග ගේම් එක", layout="wide")

# UI එක ලස්සන කිරීම (බොත්තම් එක පේළියට සහ අකුරු ලොකුවට)
st.markdown("""
    <style>
    .stButton>button {
        width: 100%;
        height: 90px;
        font-size: 30px !important;
        font-weight: bold;
        border-radius: 15px;
        background-color: #ffffff;
        border: 3px solid #0288d1;
        color: #0288d1;
    }
    h1 { font-size: 50px !important; text-align: center; color: #01579b; }
    .score-text { 
        font-size: 30px; 
        font-weight: bold; 
        text-align: center; 
        color: #1b5e20; 
        background-color: #e8f5e9;
        padding: 10px;
        border-radius: 10px;
        margin-bottom: 20px;
    }
    </style>
    """, unsafe_allow_html=True)

st.title("🥤 වතුර භාග ගේම් එක")

# Session State මගින් දත්ත සහ වත්මන් ප්‍රශ්නය ගබඩා කිරීම
if 'score' not in st.session_state: st.session_state.score = 0
if 'q_count' not in st.session_state: st.session_state.q_count = 1
if 'finished' not in st.session_state: st.session_state.finished = False

# ප්‍රශ්නයක් මුලින්ම පෙන්වන විට හෝ අලුත් ප්‍රශ්නයකට යන විට අගයන් තෝරා ගැනීම
if 'current_level' not in st.session_state:
    levels = [
        {"text": "1/4", "value": 25},
        {"text": "1/2", "value": 50},
        {"text": "3/4", "value": 75},
        {"text": "Full", "value": 100}
    ]
    shapes = [
        "border-radius: 0 0 15px 15px; width: 140px;", 
        "border-radius: 0 0 80px 80px; width: 180px;", 
        "border-radius: 40px 40px 80px 80px; width: 150px;", 
        "border-radius: 0 0 130px 130px; width: 170px;"
    ]
    st.session_state.current_level = random.choice(levels)
    st.session_state.current_shape = random.choice(shapes)

def play_sound(url):
    components.html(f"""<audio autoplay><source src="{url}" type="audio/mpeg"></audio>""", height=0)

def next_question():
    # අගයන් අලුත් කිරීම
    levels = [{"text": "1/4", "value": 25}, {"text": "1/2", "value": 50}, {"text": "3/4", "value": 75}, {"text": "Full", "value": 100}]
    shapes = ["border-radius: 0 0 15px 15px; width: 140px;", "border-radius: 0 0 80px 80px; width: 180px;", "border-radius: 40px 40px 80px 80px; width: 150px;", "border-radius: 0 0 130px 130px; width: 170px;"]
    st.session_state.current_level = random.choice(levels)
    st.session_state.current_shape = random.choice(shapes)
    st.session_state.q_count += 1
    if st.session_state.q_count > 50:
        st.session_state.finished = True
    st.rerun()

if not st.session_state.finished:
    # භාජනය පෙන්වීම
    game_html = f"""
    <div style="display: flex; justify-content: center; background: white; padding: 30px; border-radius: 30px; border: 5px solid #bbdefb; margin-bottom: 20px;">
        <div style="height: 250px; display: flex; align-items: flex-end;">
            <div style="{st.session_state.current_shape} height: 230px; border: 7px solid #263238; position: relative; overflow: hidden; background: #f1f8ff;">
                <div style="position: absolute; bottom: 0; width: 100%; height: {st.session_state.current_level['value']}%; background: linear-gradient(to top, #0288d1, #4fc3f7); transition: 0.5s;"></div>
            </div>
        </div>
    </div>
    """
    components.html(game_html, height=350)

    st.markdown(f"<p class='score-text'>ප්‍රශ්නය: {st.session_state.q_count} / 50 | ලකුණු: {st.session_state.score}</p>", unsafe_allow_html=True)

    # බොත්තම් 4 එකම පේළියකට (Columns 4)
    cols = st.columns(4)
    btn_labels = ["1/4", "1/2", "3/4", "Full"]

    for i, label in enumerate(btn_labels):
        with cols[i]:
            if st.button(label):
                if label == st.session_state.current_level['text']:
                    st.session_state.score += 1
                    play_sound("https://www.soundjay.com/misc/sounds/bell-ringing-05.mp3")
                    st.toast("නිවැරදියි! ✅")
                else:
                    play_sound("https://www.soundjay.com/buttons/sounds/button-10.mp3")
                    st.error(f"වැරදියි! පිළිතුර: {st.session_state.current_level['text']}")
                
                # පිළිතුර දුන් පසු තත්පරයකින් ඊළඟ ප්‍රශ්නයට
                import time
                time.sleep(0.5)
                next_question()

else:
    st.balloons()
    st.markdown("<h1>ක්‍රීඩාව අවසන්! 🏆</h1>", unsafe_allow_html=True)
    st.markdown(f"<p class='score-text'>මුළු ලකුණු: {st.session_state.score} / 50</p>", unsafe_allow_html=True)
    if st.button("නැවත අරඹන්න"):
        del st.session_state.current_level
        st.session_state.score = 0
        st.session_state.q_count = 1
        st.session_state.finished = False
        st.rerun()
