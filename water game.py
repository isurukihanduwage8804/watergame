import streamlit as st
import streamlit.components.v1 as components
import random
import time

# පිටුවේ සැකසුම් (layout="wide" මගින් බොත්තම් එක පේළියකට ගැනීමට ඉඩ ලබා දේ)
st.set_page_config(page_title="වතුර භාග ගේම් එක", layout="wide")

# UI එක ලස්සන කිරීම
st.markdown("""
    <style>
    .stButton>button {
        width: 100%;
        height: 100px;
        font-size: 35px !important;
        font-weight: bold;
        border-radius: 15px;
        background-color: #ffffff;
        border: 4px solid #0288d1;
        color: #0288d1;
    }
    h1 { font-size: 55px !important; text-align: center; color: #01579b; margin-bottom: 0px; }
    .score-container {
        font-size: 32px;
        font-weight: bold;
        text-align: center;
        background-color: #e3f2fd;
        padding: 15px;
        border-radius: 15px;
        color: #0d47a1;
        margin-bottom: 20px;
    }
    </style>
    """, unsafe_allow_html=True)

st.title("🥤 වතුර භාග ගේම් එක")

# Session State මගින් දත්ත පවත්වා ගැනීම
if 'score' not in st.session_state: st.session_state.score = 0
if 'q_count' not in st.session_state: st.session_state.q_count = 1
if 'finished' not in st.session_state: st.session_state.finished = False

# මට්ටම් සහ හැඩයන් (Variables)
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

# ප්‍රශ්නයක් තෝරාගෙන නොමැති නම් පමණක් අලුත් එකක් තෝරන්න
if 'current_level' not in st.session_state:
    st.session_state.current_level = random.choice(levels)
    st.session_state.current_shape = random.choice(shapes)

def play_sound(url):
    components.html(f"""<audio autoplay><source src="{url}" type="audio/mpeg"></audio>""", height=0)

if not st.session_state.finished:
    # ලකුණු පෙන්වීම
    st.markdown(f"<div class='score-container'>ප්‍රශ්නය: {st.session_state.q_count} / 50 | ලකුණු: {st.session_state.score}</div>", unsafe_allow_html=True)

    # භාජනය පෙන්වීම
    game_html = f"""
    <div style="display: flex; justify-content: center; background: white; padding: 40px; border-radius: 35px; border: 6px solid #bbdefb; margin: auto; max-width: 500px;">
        <div style="height: 250px; display: flex; align-items: flex-end;">
            <div style="{st.session_state.current_shape} height: 230px; border: 8px solid #263238; position: relative; overflow: hidden; background: #f1f8ff;">
                <div style="position: absolute; bottom: 0; width: 100%; height: {st.session_state.current_level['value']}%; background: linear-gradient(to top, #0288d1, #4fc3f7); transition: 0.5s;"></div>
            </div>
        </div>
    </div>
    """
    components.html(game_html, height=380)

    # බොත්තම් 4 එකම පේළියකට
    st.write("### නිවැරදි භාගය තෝරන්න:")
    cols = st.columns(4)
    options = ["1/4", "1/2", "3/4", "Full"]

    for i, opt in enumerate(options):
        with cols[i]:
            if st.button(opt, key=f"btn_{opt}"):
                if opt == st.session_state.current_level['text']:
                    st.session_state.score += 1
                    play_sound("https://www.soundjay.com/misc/sounds/bell-ringing-05.mp3")
                    st.toast("නිවැරදියි! ✅")
                else:
                    play_sound("https://www.soundjay.com/buttons/sounds/button-10.mp3")
                    st.error(f"වැරදියි! නිවැරදි පිළිතුර: {st.session_state.current_level['text']}")
                
                # තත්පර 0.8 කට පසු ඊළඟ ප්‍රශ්නයට යන්න
                time.sleep(0.8)
                st.session_state.q_count += 1
                if st.session_state.q_count > 50:
                    st.session_state.finished = True
                else:
                    # අලුත් ප්‍රශ්නයක් සකස් කිරීම
                    st.session_state.current_level = random.choice(levels)
                    st.session_state.current_shape = random.choice(shapes)
                st.rerun()

else:
    st.balloons()
    st.markdown("<h1>ක්‍රීඩාව අවසන්! 🏆</h1>", unsafe_allow_html=True)
    st.markdown(f"<div class='score-container'>මුළු ලකුණු: {st.session_state.score} / 50</div>", unsafe_allow_html=True)
    if st.button("නැවත අරඹන්න"):
        st.session_state.score = 0
        st.session_state.q_count = 1
        st.session_state.finished = False
        if 'current_level' in st.session_state: del st.session_state.current_level
        st.rerun()
