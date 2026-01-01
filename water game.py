import streamlit as st
import streamlit.components.v1 as components
import random

st.set_page_config(page_title="වතුර භාග ගේම් එක", layout="centered")

# UI එක ලස්සන කිරීම සහ අකුරු ලොකු කිරීම
st.markdown("""
    <style>
    .stButton>button {
        width: 100%;
        height: 85px;
        font-size: 28px !important;
        font-weight: bold;
        border-radius: 20px;
        background-color: #f8f9fa;
        border: 2px solid #0288d1;
        transition: 0.3s;
    }
    .stButton>button:hover {
        background-color: #0288d1;
        color: white;
    }
    h1 { font-size: 48px !important; text-align: center; color: #0288d1; font-weight: 800; }
    h3 { font-size: 32px !important; text-align: center; margin-top: 10px; }
    .score-text { font-size: 26px; font-weight: bold; text-align: center; color: #2e7d32; }
    </style>
    """, unsafe_allow_html=True)

st.title("🥤 වතුර භාග ගේම් එක")

# Session State මගින් දත්ත මතක තබා ගැනීම
if 'score' not in st.session_state: st.session_state.score = 0
if 'q_count' not in st.session_state: st.session_state.q_count = 1
if 'finished' not in st.session_state: st.session_state.finished = False

# ශබ්ද ක්‍රියාත්මක කරන function එක
def play_sound(url):
    components.html(f"""
        <audio autoplay>
            <source src="{url}" type="audio/mpeg">
        </audio>
    """, height=0)

if not st.session_state.finished:
    # භාජන හැඩයන්
    shapes = [
        "border-radius: 0 0 10px 10px; width: 130px;", 
        "border-radius: 0 0 70px 70px; width: 170px;", 
        "border-radius: 30px 30px 70px 70px; width: 140px;", 
        "border-radius: 0 0 120px 120px; width: 160px; height: 110px;"
    ]
    # වතුර මට්ටම්
    levels = [
        {"text": "1/4", "value": 25},
        {"text": "1/2", "value": 50},
        {"text": "3/4", "value": 75},
        {"text": "Full", "value": 100}
    ]

    # අහඹු ලෙස අගයන් තෝරා ගැනීම
    selected_shape = random.choice(shapes)
    selected_level = random.choice(levels)

    # භාජනය පෙන්වීම
    game_html = f"""
    <div style="display: flex; flex-direction: column; align-items: center; background: #ffffff; padding: 40px; border-radius: 30px; border: 4px solid #bbdefb; box-shadow: 0 10px 20px rgba(0,0,0,0.05);">
        <div style="height: 230px; display: flex; align-items: flex-end; margin-bottom: 10px;">
            <div style="{selected_shape} height: 210px; border: 6px solid #37474f; position: relative; overflow: hidden; background: rgba(230,243,255,0.5);">
                <div style="position: absolute; bottom: 0; width: 100%; height: {selected_level['value']}%; background: linear-gradient(to top, #0091ea, #81d4fa); transition: 0.8s ease-out;"></div>
            </div>
        </div>
    </div>
    """
    components.html(game_html, height=350)

    st.markdown(f"### ප්‍රශ්නය: {st.session_state.q_count} / 50")
    st.markdown(f"<p class='score-text'>ඔබේ ලකුණු: {st.session_state.score}</p>", unsafe_allow_html=True)

    # බොත්තම් පේළි 2කට
    col1, col2 = st.columns(2)
    col3, col4 = st.columns(2)
    
    def check_ans(ans_text, correct_text):
        if ans_text == correct_text:
            st.session_state.score += 1
            play_sound("https://www.soundjay.com/misc/sounds/bell-ringing-05.mp3")
            st.toast("නිවැරදියි! 🌟", icon="✅")
        else:
            play_sound("https://www.soundjay.com/buttons/sounds/button-10.mp3")
            st.error(f"වැරදියි! නිවැරදි පිළිතුර: {correct_text}")
        
        st.session_state.q_count += 1
        if st.session_state.q_count > 50:
            st.session_state.finished = True
        st.rerun()

    with col1:
        if st.button("1/4"): check_ans("1/4", selected_level['text'])
    with col2:
        if st.button("1/2"): check_
