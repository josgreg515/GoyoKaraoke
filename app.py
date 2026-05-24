import streamlit as st
import whisper
import os

# --- 1. CONFIGURACIÓN PREMIUM ---
st.set_page_config(page_title="GoyoArtista Pro", layout="centered")

st.markdown("""
    <style>
    /* Fondo Oscuro Elegante */
    .stApp {
        background: radial-gradient(circle at top, #0f172a, #020617);
        color: white;
    }
    
    /* Contenedor principal con efecto de vidrio */
    .main-container {
        background: rgba(255, 255, 255, 0.03);
        backdrop-filter: blur(15px);
        border: 1px solid rgba(212, 175, 55, 0.3);
        border-radius: 20px;
        padding: 30px;
        margin-top: 20px;
    }

    /* Títulos Dorados */
    h1 { color: #D4AF37 !important; text-align: center; font-size: 2.5rem !important; }
    h2 { color: #D4AF37 !important; text-align: center; }
    
    /* Botón Dorado */
    .stButton>button {
        background: linear-gradient(90deg, #D4AF37, #FFD700) !important;
        color: black !important;
        border-radius: 50px !important;
        font-weight: bold !important;
        width: 100% !important;
        border: none !important;
    }
    </style>
""", unsafe_allow_html=True)

# --- 2. INTERFAZ VISUAL ---
st.markdown("<h1>GOYOARTISTA</h1>", unsafe_allow_html=True)
st.markdown("<h2 style='font-size: 1.2rem;'>PORTFOLIO DE COMPOSICIÓN PRO</h2>", unsafe_allow_html=True)

# Envolvemos todo en una columna centrada
with st.container():
    st.markdown('<div class="main-container">', unsafe_allow_html=True)
    
    st.subheader("🎙️ Entrada de Audio")
    archivo = st.file_uploader("Sube tu archivo (MP3/WAV)", type=["mp3", "wav"])
    
    if archivo:
        if st.button("🚀 GENERAR FICHA TÉCNICA"):
            with open("temp.mp3", "wb") as f: f.write(archivo.read())
            with st.spinner("Procesando..."):
                model = whisper.load_model("base")
                result = model.transcribe("temp.mp3", language="es")
                st.session_state.letra = result["text"]
                st.session_state.listo = True
    
    if "listo" in st.session_state:
        st.markdown("---")
        st.write("**Letra detectada:**")
        st.text_area("", st.session_state.letra, height=200)
        st.download_button("📥 DESCARGAR FICHA TÉCNICA", st.session_state.letra, "Ficha_Tecnica.txt")
        
    st.markdown('</div>', unsafe_allow_html=True)
