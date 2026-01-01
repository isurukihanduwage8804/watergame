import streamlit as st
import streamlit.components.v1 as components
import random
import time

# පිටුවේ සැකසුම්
st.set_page_config(page_title="වතුර භාග ගේම් එක", layout="wide")

# CSS මගින් UI එක සහ බොත්තම් සැකසීම
st.markdown("""
    <style>
    .stButton>button {
        width: 100%;
        height: 85px;
        font-size: 28px !important;
        font-weight: bold;
        border-radius: 12px;
        background-color: #ffffff;
        border: 3px solid #0288d1;
        color: #0288d1;
        margin-bottom: 10px;
    }
    h1 { font-size: 45px !important; text-align: center; color: #01579b; }
    .score-container {
        font-size: 28px;
        font-weight: bold;
        text-align: center;
        background-color: #e3f2fd;
        padding: 12px;
        border-radius: 15px;
        color: #0d47a1;
        margin-bottom: 15px;
    }
    </style>
    """, unsafe_allow_html=True)

st.title("🥤 ඉරි සහිත වතුර භාග ගේම් එක")

# Session State මගින් දත්ත පවත්වා ගැනීම
if 'score' not in st.session_state: st.session_state.score = 0
if 'q_count' not in st.session_state: st.session_state.q_count = 1
if 'finished' not in st.session_state: st.session_state.finished = False

# භාග වර්ග 8ක්
levels = [
    {"text": "1/8", "value": 12.5}, {"text": "1/4", "value": 25},
    {"text": "3/8", "value": 37.5}, {"text": "1/2", "value": 50},
    {"text": "5/8", "value": 62.5}, {"text": "3/4", "value": 75},
    {"text": "7/8", "value": 87.5}, {"text": "Full", "value": 100}
]

# භාජන හැඩයන්
shapes = [
    "border-radius: 0 0 15px 15px; width: 140px;", 
    "border-radius: 0 0 80px 80px; width: 180px;", 
    "border-radius: 40px 40px 80px 80px; width: 150px;", 
    "border-radius: 0 0 130px 130px; width: 170px;"
]

# අලුත් ප්‍රශ්නයක් තෝරා ගැනීම
if 'current_level' not in st.session_state:
    st.session_state.current_level = random.choice(levels)
    st.session_state.current_shape = random.choice(shapes)

def play_sound(url):
    components.html(f'<audio autoplay><source src="{url}" type="audio/mpeg"></audio>', height=0)

if not st.session_state.finished:
    # ලකුණු පුවරුව
    st.markdown(f"<div class='score-container'>ප්‍රශ්නය: {st.session_state.q_count} / 50 | ලකුණු: {st.session_state.score}</div>", unsafe_allow_html=True)

    # භාජනය සහ ඉරි (Markings) පෙන්වීම
    level_val = st.session_state.current_level['value']
    shape_val = st.session_state.current_shape
    
    # මෙහි background එකේ 'linear-gradient' මගින් තිරස් ඉරි 8ක් මවා ඇත
    html_code = f"""
    <div style="display: flex; justify-content: center; background: white; padding: 30px; border-radius: 30px; border: 5px solid #bbdefb; margin: auto; max-width: 500px;">
        <div style="height: 250px; display: flex; align-items: flex-end;">
            <div style="{shape_val} height: 240px; border: 8px solid #263238; position: relative; overflow: hidden; 
                        background-image: linear-gradient(to bottom, transparent 96%, #555 96%); 
                        background-size: 100% 30px; background-color: #f1f8ff;">
                
                <div style="position: absolute; bottom: 0; width: 100%; height: {level_val}%; 
                            background: rgba(2, 136, 209, 0.7); transition: 0.5s;"></div>
                
                <div style="position: absolute; top: 0; left: 0; width: 100%; height: 100%; 
                            background-image: linear-gradient(to top, rgba(0,0,0,0.2) 1px, transparent 1px); 
                            background-size: 100% 12.5%; pointer-events: none;"></div>
            </div>
        </div>
    </div>
    """
    components.html(html_code, height=360)

    st.write("### ඉරි ගණන් කර නිවැරදි භාගය තෝරන්න:")
    
    # බොත්තම් 8 පේළි 2කට
    row1 = st.columns(4)
    row2 = st.columns(4)
    options = ["1/8", "1/4", "3/8", "1/2", "5/8", "3/4", "7/8", "Full"]

    for i, opt in enumerate(options):
        with (row1[i] if i < 4 else row2[i-4]):
            if st.button(opt, key=f"btn_{opt}"):
                if opt == st.session_state.current_level['text']:
                    st.session_state.score += 1
                    play_sound("https://www.soundjay.com/misc/sounds/bell-ringing-05.mp3")
                    st.toast("නිවැරදියි! ✅")
                else:
                    play_sound("https://www.soundjay.com/buttons/sounds/button-10.mp3")
                    st.error(f"වැරදියි! පිළිතුර: {st.session_state.current_level['text']}")
                
                time.sleep(0.8
