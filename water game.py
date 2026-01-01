import streamlit as st
import streamlit.components.v1 as components
import random

st.set_page_config(page_title="වතුර භාග ගේම් එක", layout="centered")

st.title("🥤 වතුර භාග ගේම් එක")
st.write("භාජනයේ හැඩය සහ වතුර ප්‍රමාණය අනුව නිවැරදි භාගය තෝරන්න.")

# Game Logic සඳහා Session State භාවිතා කිරීම
if 'score' not in st.session_state:
    st.session_state.score = 0
if 'q_count' not in st.session_state:
    st.session_state.q_count = 1
if 'finished' not in st.session_state:
    st.session_state.finished = False

# ප්‍රශ්න 50 අවසාන දැයි බැලීම
if st.session_state.q_count > 50:
    st.session_state.finished = True

if not st.session_state.finished:
    # අහඹු ලෙස හැඩයක් සහ මට්ටමක් තෝරාගැනීම
    shapes = [
        "border-radius: 0 0 10px 10px; width: 100px;", # Normal
        "border-radius: 0 0 50px 50px; width: 150px;", # Wide
        "border-radius: 0 0 5px 5px; width: 60px;",   # Thin
        "border-radius: 20px 20px 50px 50px; width: 120px;", # Bottle
        "border-radius: 0 0 100px 100px; width: 140px; height: 100px;" # Bowl
    ]
    
    levels = [
        {"text": "1/4", "value": 25},
        {"text": "1/2", "value": 50},
        {"text": "3/4", "value": 75},
        {"text": "Full", "value": 100}
    ]

    # හැම refresh එකකදීම අලුත් අගයන් ගැනීම සඳහා
    selected_shape = random.choice(shapes)
    selected_level = random.choice(levels)

    # HTML සහ CSS මගින් භාජනය පෙන්වීම
    game_html = f"""
    <div style="display: flex; flex-direction: column; align-items: center; justify-content: center; background: #f0f2f6; padding: 20px; border-radius: 15px;">
        <div style="height: 200px; display: flex; align-items: flex-end; margin-bottom: 20px;">
            <div style="{selected_shape} height: 180px; border: 4px solid #333; position: relative; overflow: hidden; background: white;">
                <div style="position: absolute; bottom: 0; width: 100%; height: {selected_level['value']}%; background: linear-gradient(to top, #2196F3, #64B5F6); transition: 0.5s;"></div>
            </div>
        </div>
        <h3 style="font-family: sans-serif; color: #333;">ප්‍රශ්නය: {st.session_state.q_count} / 50</h3>
    </div>
    """
    
    components.html(game_html, height=300)

    # ලකුණු පුවරුව
    st.sidebar.metric("ඔබේ ලකුණු", st.session_state.score)

    # පිළිතුරු ලබාදෙන බොත්තම්
    col1, col2, col3, col4 = st.columns(4)
    
    def check_ans(ans_text, correct_text):
        if ans_text == correct_text:
            st.session_state.score += 1
            st.toast("නිවැරදියි! 🎉")
        else:
            st.error(f"වැරදියි! නිවැරදි පිළිතුර: {correct_text}")
        st.session_state.q_count += 1

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
    st.success(f"ක්‍රීඩාව අවසන්! ඔබේ මුළු ලකුණු ප්‍රමාණය: {st.session_state.score} / 50")
    if st.button("නැවත අරඹන්න"):
        st.session_state.score = 0
        st.session_state.q_count = 1
        st.session_state.finished = False
        st.rerun()
