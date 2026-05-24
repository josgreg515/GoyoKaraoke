import streamlit as st
import whisper
import os

# --- 1. DISEÑO PREMIUM ---
def aplicar_estilo_goyo():
    st.markdown("""
        <style>
        .stApp { background: linear-gradient(rgba(0,0,0,0.8), rgba(0,0,0,0.8)); color: white; }
        .stButton>button { background-color: #28a745 !important; color: white !important; border-radius: 30px; }
        </style>
    """, unsafe_allow_html=True)

aplicar_estilo_goyo()

# --- 2. CABECERA ---
col1, col2, col3 = st.columns([1,2,1])
with col2:
    if os.path.exists("logo.png"): st.image("logo.png")
    else: st.title("🎼 GoyoArtista")

st.markdown("### Generador de Ficha Técnica")

# --- 3. PROCESAMIENTO ---
archivo = st.file_uploader("Sube tu canción (MP3/WAV):", type=["mp3", "wav"])

if archivo:
    with open("audio_temp.mp3", "wb") as f: f.write(archivo.read())
    
    if st.button("🚀 GENERAR FICHA TÉCNICA"):
        with st.spinner("Analizando composición..."):
            model = whisper.load_model("base")
            result = model.transcribe("audio_temp.mp3", language="es")
            
            # Organización de datos
            letra = result["text"]
            duracion = "Aprox. " + str(round(len(letra.split()) * 0.4)) + " segundos"
            
            st.success("¡Ficha generada!")
            
            # Mostrar Ficha
            st.markdown("---")
            st.subheader("📋 Resumen de la Obra")
            st.write(f"**Duración estimada:** {duracion}")
            st.write(f"**Conteo de palabras:** {len(letra.split())}")
            
            st.subheader("✍️ Letra")
            st.text_area("Transcripción:", letra, height=200)
            
            st.download_button("📥 Descargar Ficha en TXT", letra, "Ficha_Tecnica.txt")
