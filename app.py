import streamlit as st
import os
import uuid

st.set_page_config(page_title="궁극기 리얼 임팩트 시뮬레이터", page_icon="💥")

st.title("💥 오버워치 궁극기 콤보 시뮬레이터")
st.write("버튼을 누르고 화면과 소리를 즐기세요!")

# 로컬 GIF 움짤과 다운받은 MP3 파일 매핑
assets = {
    "겐지": {"gif": "genji.gif", "audio": "genji.mp3"},
    "트레이서": {"gif": "tracer.gif", "audio": "tracer.mp3"},
    "라인하르트": {"gif": "reinhardt.gif", "audio": "reinhardt.mp3"}
}

character = st.selectbox(
    "어떤 캐릭터를 고르시겠습니까?",
    list(assets.keys())
)

st.divider()

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
    
    # 1. 시각 효과(CSS) 주입
    st.markdown(get_css_effects(character, run_id), unsafe_allow_html=True)
    
    # 2. 오디오 재생 (스트림릿 기본 오디오 플레이어 + 자동재생)
    audio_file = assets[character]["audio"]
    if os.path.exists(audio_file):
        # PC에서는 자동 재생, 모바일에서는 재생 버튼을 직접 누를 수 있게 플레이어 노출
        st.audio(audio_file, format="audio/mpeg", autoplay=True)
    else:
        st.toast(f"🔇 {audio_file} 파일이 폴더에 없습니다!", icon="⚠️")
        
    # 3. 움짤(GIF) 재생 (자막 삭제 완료)
    gif_file = assets[character]["gif"]
    if os.path.exists(gif_file):
        st.image(gif_file, use_container_width=True)
    else:
        st.info(f"💡 {gif_file} 파일을 폴더에 넣어주세요!")
