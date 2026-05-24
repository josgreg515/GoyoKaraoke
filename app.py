import streamlit as st
import whisper
import os

# --- 1. CONFIGURACIÓN VISUAL PREMIUM ---
st.set_page_config(page_title="GoyoArtista Pro", layout="wide")

st.markdown("""
    <style>
    /* Fondo con gradiente profundo y elegante */
    .stApp {
        background: linear-gradient(135deg, #050a18 0%, #1c2541 100%);
        color: #ffffff;
    }
    
    /* El contenedor "Glass" (Vidrio Esmerilado) */
    .glass-card {
        background: rgba(255, 255, 255, 0.03);
        backdrop-filter: blur(20px);
        -webkit-backdrop-filter: blur(20px);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 25px;
        padding: 40px;
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.8);
    }

    /* Botón estilo Dorado */
    .stButton>button {
        background: linear-gradient(90deg, #D4AF37 0%, #FFD700 100%) !important;
        color: #000000 !important;
        border-radius: 50px !important;
        font-weight: 800 !important;
        text-transform: uppercase !important;
        width: 100% !important;
        height: 60px !important;
        border: none !important;
    }
    
    /* Tipografía */
    h1 { color: #FFD700 !important; text-align: center; font-size: 3rem; margin-bottom: 0px !important; }
    h3 { color: #FFFFFF !important; }
    </style>
""", unsafe_allow_html=True)

# --- 2. INTERFAZ ---
st.markdown("<h1>GOYOARTISTA</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center; color:#FFD700;'>PORTFOLIO DE COMPOSICIÓN PRO</p>", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

col1, col2 = st.columns([1, 1.5])

with col1:
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.subheader("🎙️ Entrada de Audio")
    archivo = st.file_uploader("Sube tu archivo (MP3/WAV)", type=["mp3", "wav"])
    
    if archivo:
        if st.button("🚀 GENERAR FICHA TÉCNICA"):
            with open("temp.mp3", "wb") as f: f.write(archivo.read())
            with st.spinner("Procesando sonido..."):
                model = whisper.load_model("base")
                result = model.transcribe("temp.mp3", language="es")
                st.session_state.letra = result["text"]
                st.session_state.listo = True
    st.markdown('</div>', unsafe_allow_html=True)

with col2:
    if "listo" in st.session_state:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.subheader("📋 Resultado Técnico")
        st.write(f"**Palabras:** {len(st.session_state.letra.split())}")
        st.text_area("Letra extraída:", st.session_state.letra, height=200)
        st.download_button("📥 DESCARGAR FICHA", st.session_state.letra, "Ficha_Goyo.txt")
        st.markdown('</div>', unsafe_allow_html=True)
