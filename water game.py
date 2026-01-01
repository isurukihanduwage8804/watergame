import streamlit as st
import streamlit.components.v1 as components
import random

# පිටුවේ සැකසුම්
st.set_page_config(page_title="වතුර භාග ගේම් එක", layout="centered")

# UI එක සහ අකුරු ඉතා ලොකුවට සැකසීම (Custom CSS)
st.markdown("""
    <style>
    /* බොත්තම් වල අකුරු සහ ප්‍රමාණය */
    .stButton>button {
        width: 100%;
        height: 100px;
        font-size: 35px !important; /* අකුරු ඉතා ලොකු කර ඇත */
        font-weight: bold;
        border-radius: 20px;
        background-color: #ffffff;
        border: 3px solid #0288d1;
        color: #0288d1;
        transition: 0.3s;
    }
    .stButton>button:hover {
        background-color: #0288d1;
        color: white;
    }
    /* මාතෘකා */
    h1 { font-size: 55px !important; text-align: center; color: #01579b; }
    h3 { font-size: 35px !important; text-align: center; }
    /* ලකුණු පුවරුව */
    .score-text { 
        font-size: 32px; 
        font-weight: bold; 
        text-align: center; 
        color: #1b5e20; 
        background-color: #e8f5e9;
        padding: 10px;
        border-radius: 10px;
    }
    </style>
    """, unsafe_allow_html=True)

st.title("🥤 වතුර භාග ගේම් එක")

# දත්ත මතක තබා ගැනීමට Session State භාවිතා කිරීම
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

# ප්‍රශ්න පෙන්වන ප්‍රධාන කොටස
if not st.session_state.finished:
    # භාජන හැඩයන් (අහඹු ලෙස වෙනස් වේ)
    shapes = [
        "border-radius: 0 0 15px 15px; width: 140px;", 
        "border-radius: 0 0 80px 80px; width: 180px;", 
        "border-radius: 40px 40px 80px 80px; width: 150px;", 
        "border-radius: 0 0 130px 130px; width: 170px; height: 120px;"
    ]
    # වතුර මට්ටම්
    levels = [
        {"text": "1/4", "value": 25},
        {"text": "1/2", "value": 50},
        {"text": "3/4", "value": 75},
        {"text": "Full", "value": 100}
    ]

    # අහඹු ලෙස එකක් තෝරා ගැනීම
    selected_shape = random.choice(shapes)
    selected_level = random.choice(levels)

    # භාජනයේ රූපය (HTML/CSS)
    game_html = f"""
    <div style="display: flex; flex-direction: column; align-items: center; background: white; padding: 40px; border-radius: 35px; border: 5px solid #bbdefb;">
        <div style="height: 250px; display: flex; align-items: flex-end; margin-bottom: 10px;">
            <div style="{selected_shape} height: 230px; border: 7px solid #263238; position: relative; overflow: hidden; background: rgba(230,243,255,0.4);">
                <div style="position: absolute; bottom: 0; width: 100%; height: {selected_level['value']}%; background: linear-gradient(to top, #0288d1, #4fc3f7); transition: 0.8s ease-out;"></div>
            </div>
        </div>
    </div>
    """
    components.html(game_html, height=380)

    st.markdown(f"### ප්‍රශ්නය: {st.session_state.q_count} / 50")
    st.markdown(f"<p class='score-text'>ලකුණු: {st.session_state.score}</p>", unsafe_allow_html=True)

    # පිළිතුරු පරීක්ෂා කරන function එක
    def check_ans(ans_text, correct_text):
        if ans_text == correct_text:
            st.session_state.score += 1
            play_sound("https://www.soundjay.com/misc/sounds/bell-ringing-05.mp3")
            st.toast("නිවැරදියි! ✅")
        else:
            play_sound("https://www.soundjay.com/buttons/sounds/button-10.mp3")
            st.error(f"වැරදියි! නිවැරදි පිළිතුර: {correct_text}")
        
        st.session_state.q_count += 1
        if st.session_state.q_count > 50:
            st.session_state.finished = True
        st.rerun()

    # බොත්තම් (Buttons)
    col1, col2 = st.columns(2)
    col3, col4 = st.columns(2)
    
    with col1:
        if st.button("1/4"): check_ans("1/4", selected_level['text'])
    with col2:
        if st.button("1/2"): check_ans("1/2", selected_level['text'])
    with col3:
        if st.button("3/4"): check_ans("3/4", selected_level['text'])
    with col4:
        if st.button("Full"): check_ans("Full", selected_level['text'])

else:
    # ගේම් එක අවසානයේ පෙන්වන තිරය
    st.balloons()
    st.markdown("<h1>ක්‍රීඩාව අවසන්! 🏆</h1>", unsafe_allow_html=True)
    st.markdown(f"<p class='score-text' style='font-size:40px;'>මුළු ලකුණු: {st.session_state.score} / 50</p>", unsafe_allow_html=True)
    if st.button("නැවත අරඹන්න"):
        st.session_state.score = 0
        st.session_state.q_count = 1
        st.session_state.finished = False
        st.rerun()
