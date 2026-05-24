import streamlit as st
import os
import yt_dlp

# --- 1. DISEÑO PREMIUM ---
def aplicar_estilo_goyo():
    fondo_url = "https://images.unsplash.com/photo-1493225255756-d9584f8606e9?q=80&w=1920"
    st.markdown(f"""
        <style>
        .stApp {{ background: linear-gradient(rgba(0,0,0,0.7), rgba(0,0,0,0.7)), url("{fondo_url}"); background-size: cover; }}
        /* Botón de descarga en verde */
        div.stButton > button:nth-child(1) {{ 
            background-color: #28a745 !important; 
            color: white !important; 
            border-radius: 30px; 
            height: 3em; 
            font-weight: bold;
        }}
        h1, h2, h3, p {{ color: white !important; }}
        </style>
    """, unsafe_allow_html=True)

aplicar_estilo_goyo()

# --- 2. LOGO ---
col1, col2, col3 = st.columns([1,2,1])
with col2:
    if os.path.exists("logo.png"): st.image("logo.png")
    else: st.title("📥 GoyoDownloader")

# --- 3. LÓGICA DE DESCARGA ---
url = st.text_input("Pega el enlace de YouTube aquí:")

if url:
    try:
        st.video(url)
        formato = st.radio("¿Qué deseas descargar?", ("Video (MP4)", "Solo Audio (MP3)"))
        
        if st.button("🚀 INICIAR DESCARGA"):
            barra = st.progress(0)
            st.write("🔄 Iniciando conexión segura...")
            
            # Configuración potente para evitar bloqueos
            ydl_opts = {
                'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best' if formato == "Video (MP4)" else 'bestaudio/best',
                'outtmpl': 'descarga_final.%(ext)s',
                'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
            }
            
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                barra.progress(50)
                ydl.download([url])
                
            barra.progress(100)
            archivo = "descarga_final.mp4" if formato == "Video (MP4)" else "descarga_final.webm"
            
            if os.path.exists(archivo):
                st.success("¡Descarga completada!")
                with open(archivo, "rb") as f:
                    st.download_button("📥 DESCARGAR ARCHIVO", f, file_name=f"Goyo_{'video' if formato == 'Video (MP4)' else 'audio'}.{'mp4' if formato == 'Video (MP4)' else 'mp3'}")
            else:
                st.error("El archivo no se pudo generar. Intenta con otro video.")

    except Exception as e:
        st.error(f"Error técnico: {e}. YouTube está bloqueando la conexión. Intenta nuevamente.")
