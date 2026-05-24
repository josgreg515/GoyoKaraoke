import streamlit as st
import whisper
import os

# --- DISEÑO ---
st.set_page_config(page_title="GoyoProcesador", layout="centered")
st.markdown("""
    <style>
    .stApp { background: linear-gradient(rgba(0,0,0,0.8), rgba(0,0,0,0.8)); color: white; }
    .stButton>button { background-color: #28a745 !important; color: white !important; border-radius: 30px; }
    </style>
""", unsafe_allow_html=True)

st.title("🎛️ GoyoProcesador Pro")
st.info("Sube un video o audio de tu dispositivo para procesar.")

# --- LÓGICA ---
archivo = st.file_uploader("Sube tu archivo (MP4/MP3):", type=["mp4", "mp3", "wav"])

if archivo:
    # Guardar temporalmente
    with open("temp_file", "wb") as f: f.write(archivo.read())
    
    if st.button("🚀 PROCESAR ARCHIVO"):
        with st.spinner("Analizando contenido..."):
            model = whisper.load_model("base")
            result = model.transcribe("temp_file", language="es")
            st.session_state.letra = result["text"]
            st.success("¡Archivo procesado con éxito!")

if "letra" in st.session_state:
    st.text_area("Letra extraída:", st.session_state.letra, height=300)
    st.download_button("📥 Descargar Letra", st.session_state.letra, "letra.txt")
