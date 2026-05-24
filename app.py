# --- 3. CONFIGURACIÓN ---
# ... (tu código anterior hasta el file_uploader) ...

if audio_file is not None:
    ruta_audio = os.path.abspath("temp_audio.mp3")
    with open(ruta_audio, "wb") as f:
        f.write(audio_file.getbuffer())

    # Paso 1: Transcribir (se activa al subir el archivo)
    if "letra" not in st.session_state:
        st.session_state.letra = ""

    if st.button("👂 1. ANALIZAR LETRA"):
        with st.spinner("Escuchando..."):
            model = whisper.load_model("base")
            result = model.transcribe(ruta_audio)
            st.session_state.letra = result["text"]

    # Paso 2: Edición (aparece solo si ya hay letra)
    if st.session_state.letra:
        st.markdown("### ✍️ Corrige la letra si es necesario:")
        st.session_state.letra = st.text_area("Letra editada:", st.session_state.letra, height=200)

        # Paso 3: Generar Video (se activa solo cuando la letra está lista)
        if st.button("🚀 2. GENERAR VIDEO FINAL"):
            with st.spinner("Diseñando tu video..."):
                # Aquí va tu lógica de renderizado actual
                # (Usando el 'video_final = fondo_video' que definimos antes)
                # ...
                st.success("¡Video listo!")
                st.video(archivo_salida)
