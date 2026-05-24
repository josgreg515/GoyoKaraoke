import streamlit as st
import whisper
import os

# --- 1. CONFIGURACIÓN PREMIUM ---
st.set_page_config(page_title="GoyoArtista Pro", layout="wide")

st.markdown("""
    <style>
    .stApp {
        background: linear-gradient(-45deg, #050a18, #1c2541, #0a1128, #001219);
        color: #ffffff;
    }
    .glass-card {
        background: rgba(255, 255, 255, 0.05);
        backdrop-filter: blur(15px);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 20px;
        padding: 30px;
    }
    .stButton>button {
        background: linear-gradient(90deg, #FFD700, #FFCC00) !important;
        color: #000000 !important;
        border-radius: 50px !important;
        font-weight: bold !important;
        width: 100% !important;
    }
    h1 { color: #FFD700 !important; text-align: center; }
    </style>
""", unsafe_allow_html=True)

# --- 2. INTERFAZ ---
st.markdown("<h1>GOYO<span>ARTISTA</span></h1>", unsafe_allow_html=True)

col_l, col_r = st.columns([1, 1.5])

with col_l:
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.subheader("🎙️ Entrada de Audio")
    archivo = st.file_uploader("Sube tu archivo (MP3/WAV)", type=["mp3", "wav"])
    
    if archivo:
        if st.button("🚀 GENERAR FICHA TÉCNICA"):
            with open("temp.mp3", "wb") as f: f.write(archivo.read())
            with st.spinner("Analizando..."):
                model = whisper.load_model("base")
                result = model.transcribe("temp.mp3", language="es")
                st.session_state.letra = result["text"]
                st.session_state.listo = True
    st.markdown('</div>', unsafe_allow_html=True)

with col_r:
    if "listo" in st.session_state:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.subheader("📋 Ficha Técnica")
        st.metric("Palabras", len(st.session_state.letra.split()))
        st.text_area("Letra:", st.session_state.letra, height=250)
        st.download_button("📥 DESCARGAR FICHA", st.session_state.letra, "Ficha.txt")
        st.markdown('</div>', unsafe_allow_html=True)
