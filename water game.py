import streamlit as st
import streamlit.components.v1 as components
import random
import time

# පිටුවේ සැකසුම්
st.set_page_config(page_title="වතුර භාග ගේම් එක", layout="wide")

# CSS මගින් UI එක සැකසීම
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

st.title("🥤 Advance වතුර භාග ගේම් එක")

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

# ප්‍රශ්නයක් තෝරා නොමැති නම් අලුත් එකක් ගැනීම
if 'current_level' not in st.session_state:
    st.session_state.current_level = random.choice(levels)
    st.session_state.current_shape = random.choice(shapes)

def play_sound(url):
    components.html(f'<audio autoplay><source src="{url}" type="audio/mpeg"></audio>', height=0)

if not st.session_state.finished:
    # ලකුණු පුවරුව
    st.markdown(f"<div class='score-container'>ප්‍රශ්නය: {st.session_state.q_count} / 50 | ලකුණු: {st.session_state.score}</div>", unsafe_allow_html=True)

    # භාජනය පෙන්වීම (f-string වැරදි මඟහරවා ගැනීමට වෙනම variable එකකට ගෙන ඇත)
    level_val = st.session_state.current_level['value']
    shape_val = st.session_state.current_shape
    
    html_code = f"""
    <div style="display: flex; justify-content: center; background: white; padding: 30px; border-radius: 30px; border: 5px solid #bbdefb; margin: auto; max-width: 500px;">
        <div style="height: 250px; display: flex; align-items: flex-end;">
            <div style="{shape_val} height: 230px; border: 8px solid #263238; position: relative; overflow: hidden; background: #f1f8ff;">
                <div style="position: absolute; bottom: 0; width: 100%; height: {level_val}%; background: linear-gradient
