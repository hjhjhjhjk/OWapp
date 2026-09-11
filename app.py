import streamlit as st
import os
import uuid
import streamlit.components.v1 as components

st.set_page_config(page_title="궁극기 리얼 임팩트 시뮬레이터", page_icon="💥")

st.title("💥 오버워치 궁극기 콤보 시뮬레이터")
st.write("목소리 톤(Pitch)까지 캐릭터에 맞춰 커스텀 완료!")

gif_files = {
    "겐지": "genji.gif",
    "트레이서": "tracer.gif",
    "라인하르트": "reinhardt.gif"
}

character = st.selectbox(
    "어떤 캐릭터를 고르시겠습니까?",
    list(gif_files.keys())
)

st.divider()

# 목소리 변조(Pitch, Rate)가 적용된 TTS 함수
def play_tts_sound(char):
    dialogues = {
        "겐지": "류진노 켄오 쿠라에!!",
        "트레이서": "시간 좀 가속해 볼까?",
        "라인하르트": "망치 나가신다!!! 으아아아아!"
    }
    text = dialogues.get(char, "")
    
    js = f"""
    <script>
        var msg = new SpeechSynthesisUtterance("{text}");
        msg.lang = 'ko-KR';
        
        // 캐릭터별 목소리 변조 꼼수!
        if ("{char}" === "겐지") {{
            msg.pitch = 0.7; // 청년 느낌 (살짝 낮고 날렵하게)
            msg.rate = 1.3;
        }} else if ("{char}" === "트레이서") {{
            msg.pitch = 1.6; // 여성 느낌 (높고 빠르게)
            msg.rate = 1.5;
        }} else if ("{char}" === "라인하르트") {{
            msg.pitch = 0.1; // 덩치 큰 할아버지 (아주 낮고 묵직하게)
            msg.rate = 0.8;
        }}
        
        window.speechSynthesis.speak(msg);
    </script>
    """
    components.html(js, height=0)

def get_css_effects(char, run_id):
    if char == "라인하르트":
        return f"""
            <style>
            @keyframes earth-shatter-{run_id} {{
                0% {{ transform: translate(1px, 1px) rotate(0deg); }}
                10% {{ transform: translate(-50px, -50px) rotate(-5deg); }}
                20% {{ transform: translate(50px, 0px) rotate(5deg); }}
                30% {{ transform: translate(-50px, 50px) rotate(0deg); }}
                40% {{ transform: translate(50px, -50px) rotate(5deg); }}
                50% {{ transform: translate(-50px, 50px) rotate(-5deg); }}
                60% {{ transform: translate(50px, 50px) rotate(0deg); }}
                100% {{ transform: translate(1px, -1px) rotate(0deg); }}
            }}
            .stApp {{ animation: earth-shatter-{run_id} 0.5s ease-in-out !important; }}
            @keyframes fadeInOut-{run_id} {{ 0% {{ opacity: 1; }} 100% {{ opacity: 0; }} }}
            .crack-overlay-{run_id} {{
                position: fixed; top: 50%; left: 50%; transform: translate(-50%, -50%);
                width: 100vw; height: 100vh;
                background: radial-gradient(circle, transparent 20%, rgba(0,0,0,0.8) 100%);
                border: 20px solid rgba(255, 69, 0, 0.5);
                z-index: 99999; pointer-events: none; opacity: 0;
                animation: fadeInOut-{run_id} 1s forwards;
            }}
            </style>
            <div class="crack-overlay-{run_id}">&nbsp;</div>
        """
        
    elif char == "겐지":
        return f"""
            <style>
            @keyframes screen-slice-double-{run_id} {{
                0% {{ transform: translate(0, 0) skew(0deg); }}
                15% {{ transform: translate(-30px, 15px) skew(15deg); filter: contrast(200%) hue-rotate(90deg); }}
                30% {{ transform: translate(0, 0) skew(0deg); filter: none; }}
                45% {{ transform: translate(30px, -15px) skew(-15deg); filter: contrast(200%) hue-rotate(90deg); }}
                60% {{ transform: translate(0, 0) skew(0deg); filter: none; }}
                100% {{ transform: translate(0, 0) skew(0deg); filter: none; }}
            }}
            @keyframes strike-right-{run_id} {{
                0% {{ width: 0%; opacity: 1; }}
                50% {{ width: 200vw; opacity: 1; }}
                100% {{ width: 200vw; opacity: 0; }}
            }}
            @keyframes strike-left-{run_id} {{
                0% {{ width: 0%; opacity: 1; }}
                50% {{ width: 200vw; opacity: 1; }}
                100% {{ width: 200vw; opacity: 0; }}
            }}
            .stApp {{ animation: screen-slice-double-{run_id} 0.6s ease-out !important; }}
            .sword-right-{run_id} {{
                position: fixed; top: 20%; left: -50%; width: 0%; height: 20px;
                background: #39ff14; box-shadow: 0 0 20px #39ff14, 0 0 50px #ffffff;
                transform: rotate(25deg); z-index: 99999; pointer-events: none;
                animation: strike-right-{run_id} 0.3s ease-out forwards;
            }}
            .sword-left-{run_id} {{
                position: fixed; top: 70%; right: -50%; width: 0%; height: 20px;
                background: #39ff14; box-shadow: 0 0 20px #39ff14, 0 0 50px #ffffff;
                transform: rotate(-25deg); z-index: 99999; pointer-events: none;
                animation: strike-left-{run_id} 0.3s ease-out 0.25s forwards;
            }}
            </style>
            <div class="sword-right-{run_id}">&nbsp;</div>
            <div class="sword-left-{run_id}">&nbsp;</div>
        """
        
    elif char == "트레이서":
        return f"""
            <style>
            @keyframes glitch-{run_id} {{
                0% {{ filter: invert(0%) hue-rotate(0deg); transform: skew(0deg); }}
                20% {{ filter: invert(100%) hue-rotate(90deg); transform: skew(10deg); }}
                40% {{ filter: invert(0%) hue-rotate(180deg); transform: skew(-10deg); }}
                60% {{ filter: invert(100%) hue-rotate(270deg); transform: skew(5deg); }}
                80% {{ filter: invert(0%) hue-rotate(360deg); transform: skew(-5deg); }}
                100% {{ filter: invert(0%); transform: skew(0deg); }}
            }}
            .stApp {{ animation: glitch-{run_id} 0.8s ease-in-out !important; }}
            </style>
        """

if st.button(f"{character}! 풀콤보 발동 ⚡", type="primary"):
    run_id = str(uuid.uuid4())
    
    st.markdown(get_css_effects(character, run_id), unsafe_allow_html=True)
    
    # 변조된 AI 성우 재생!
    play_tts_sound(character)
    
    if character == "라인하르트":
        st.error("망치 나가신다!!! 🔨💥")
    elif character == "겐지":
        st.success("류진노 켄오 쿠라에!!! 🐉⚔️ (2연속 베기!)")
    elif character == "트레이서":
        st.warning("시간 좀 가속해 볼까? ⏳💨")
        
    file_name = gif_files[character]
    if os.path.exists(file_name):
        st.image(file_name, use_container_width=True)
    else:
        st.info(f"💡 연출을 100% 즐기려면, {file_name} 파일을 폴더에 넣어주세요!")