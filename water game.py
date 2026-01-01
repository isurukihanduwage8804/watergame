import streamlit as st
import streamlit.components.v1 as components
import random

st.set_page_config(page_title="වතුර භාග ගේම් එක", layout="centered")

# CSS මගින් අකුරු ලොකු කිරීම සහ UI එක ලස්සන කිරීම
st.markdown("""
    <style>
    .stButton>button {
        width: 100%;
        height: 80px;
        font-size: 25px !important;
        font-weight: bold;
        border-radius: 15px;
    }
    h1 { font-size: 50px !important; text-align: center; color: #0288d1; }
    h3 { font-size: 30px !important; text-align: center; }
    .score-text { font-size: 28px; font-weight: bold; text-align: center; color: #4CAF50; }
    </style>
    """, unsafe_allow_index=True)

st.title("🥤 වතුර භාග ගේම් එක")

# Session State
if 'score' not in st.session_state: st.session_state.score = 0
if 'q_count' not in st.session_state: st.session_state.q_count = 1
if 'finished' not in st.session_state: st.session_state.finished = False

# ශබ්ද ලබාගැනීම සඳහා වන Function එක (නොමිලේ ලබාදෙන ශබ්ද කිහිපයක්)
def play_sound(url):
    components.html(f"""
        <audio autoplay>
            <source src="{url}" type="audio/mpeg">
        </audio>
    """, height=0)

if not st.session_state.finished:
    # භාජන හැඩයන් සහ මට්ටම්
    shapes = [
        "border-radius: 0 0 10px 10px; width: 120px;", # Normal
        "border-radius: 0 0 60px 60px; width: 160px;", # Wide
        "border-radius: 20px 20px 60px 60px; width: 130px;", # Bottle
        "border-radius: 0 0 100px 100px; width: 150px; height: 110px;" # Bowl
    ]
    levels = [
        {"text": "1/4", "value": 25},
        {"text": "1/2", "value": 50},
        {"text": "3/4", "value": 75},
        {"text": "Full", "value": 100}
    ]

    selected_shape = random.choice(shapes)
    selected_level = random.choice(levels)

    # භාජනයේ පෙනුම
    game_html = f"""
    <div style="display: flex; flex-direction: column; align-items: center; background: #ffffff; padding: 30px; border-radius: 25px; border: 3px solid #e0e0e0;">
        <div style="height: 220px; display: flex; align-items: flex-end; margin-bottom: 10px;">
            <div style="{selected_shape} height: 200px; border: 5px solid #333; position: relative; overflow: hidden; background: rgba(255,255,255,0.8);">
                <div style="position: absolute; bottom: 0; width: 100%; height: {selected_level['value']}%; background: linear-gradient(to top, #00d2ff, #3a7bd5); transition: 0.8s;"></div>
            </div>
        </div>
    </div>
    """
    components.html(game_html, height=300)

    st.markdown(f"### ප්‍රශ්නය: {st.session_state.q_count} / 50")
    st.markdown(f"<p class='score-text'>ඔබේ ලකුණු: {st.session_state.score}</p>", unsafe_allow_index=True)

    # බොත්තම් (අකුරු ලොකුයි)
    col1, col2 = st.columns(2)
    col3, col4 = st.columns(2)
    
    def check_ans(ans_text, correct_text):
        if ans_text == correct_text:
            st.session_state.score += 1
            play_sound("https://www.soundjay.com/misc/sounds/bell-ringing-05.mp3") # Correct Sound
            st.toast("නිවැරදියි! 🌟", icon="✅")
        else:
            play_sound("https://www.soundjay.com/buttons/sounds/button-10.mp3") # Wrong Sound
            st.error(f"වැරදියි! නිවැරදි පිළිතුර: {correct_text}")
        
        st.session_state.q_count += 1
        if st.session_state.q_count > 50:
            st.session_state.finished = True
        st.rerun()

    with col1:
        if st.button("1/4"): check_ans("1/4", selected_level['text'])
    with col2:
        if st.button("1/2"): check_ans("1/2", selected_level['text'])
    with col3:
        if st.button("3/4"): check_ans("3/4", selected_level['text'])
    with col4:
        if st.button("Full"): check_ans("Full", selected_level['text'])

else:
    st.balloons()
    st.markdown("<h1>ක්‍රීඩාව අවසන්! 🏆</h1>", unsafe_allow_index=True)
    st.markdown(f"### ඔබේ මුළු ලකුණු ප්‍රමාණය: {st.session_state.score} / 50")
    if st.button("නැවත මුල සිට අරඹන්න"):
        st.session_state.score = 0
        st.session_state.q_count = 1
        st.session_state.finished = False
        st.rerun()
