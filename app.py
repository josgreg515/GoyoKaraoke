import streamlit as st
import whisper
import os

# --- 1. CONFIGURACIÓN DEL DISEÑO ---
st.set_page_config(page_title="GoyoArtista Pro", layout="centered")

st.markdown("""
    <style>
    /* Fondo estilo paisaje sutil */
    .stApp {
        background: linear-gradient(rgba(240, 245, 250, 0.9), rgba(240, 245, 250, 0.9)), 
                    url('https://images.unsplash.com/photo-1506744038136-46273834b3fb');
        background-size: cover;
    }
    
    /* Contenedor tipo "Maqueta" */
    .maqueta-card {
        background: rgba(255, 255, 255, 0.95);
        padding: 30px;
        border-radius: 15px;
        box-shadow: 0 10px 25px rgba(0,0,0,0.2);
        border: 2px solid #e0e0e0;
    }
    
    /* Títulos y Estilo */
    h1 { color: #001f3f !important; text-align: center; font-family: sans-serif; }
    h2 { color: #001f3f !important; font-size: 1rem !important; text-align: center; }
    
    .stButton>button {
        background-color: #001f3f !important;
        color: white !important;
        width: 100% !important;
        border-radius: 5px !important;
    }
    </style>
""", unsafe_allow_html=True)

# --- 2. ESTRUCTURA DE LA INTERFAZ ---
st.markdown("<h1>GOYOARTISTA</h1>", unsafe_allow_html=True)
st.markdown("<h2>PORTFOLIO DE COMPOSICIÓN PRO</h2>", unsafe_allow_html=True)

st.markdown('<div class="maqueta-card">', unsafe_allow_html=True)

# Campos de entrada alineados con tu imagen
titulo = st.text_input("Título de Canción")
artista = st.text_input("Artista")
archivo = st.file_uploader("Sube tu archivo (MP3/WAV)", type=["mp3", "wav"])

if st.button("🚀 GENERAR FICHA TÉCNICA"):
    if archivo and titulo and artista:
        with open("temp.mp3", "wb") as f: f.write(archivo.read())
        with st.spinner("Analizando..."):
            model = whisper.load_model("base")
            result = model.transcribe("temp.mp3", language="es")
            
            st.success("¡Ficha generada!")
            st.write(f"**Canción:** {titulo}")
            st.write(f"**Artista:** {artista}")
            st.text_area("Letra:", result["text"], height=150)
            st.download_button("📥 DESCARGAR FICHA", result["text"], "Ficha.txt")
    else:
        st.error("Por favor completa todos los campos y sube un audio.")

st.markdown('</div>', unsafe_allow_html=True)
