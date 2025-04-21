import os
import subprocess

# Instalar dependencias faltantes si es necesario
try:
    import moviepy.editor as mp
except ImportError:
    subprocess.check_call([os.sys.executable, "-m", "pip", "install", "moviepy==1.0.3"])

try:
    import yt_dlp
except ImportError:
    subprocess.check_call([os.sys.executable, "-m", "pip", "install", "yt_dlp"])

import streamlit as st
from utils import (
    extract_youtube_audio,
    transcribe_audio,
    detect_viral_segments,
    generate_captions,
    create_clip_with_subs
)

st.set_page_config(layout="centered", page_title="ClipVic AI", page_icon="🎬")
st.title("🎬 ClipVic AI - Viral Clip Generator")
st.write("Convierte cualquier video de YouTube en clips virales con subtítulos estilo TikTok.")

youtube_url = st.text_input("Pega el link de YouTube aquí", placeholder="https://www.youtube.com/watch?v=...")
language = st.selectbox("Idioma preferido para los subtítulos", ["Español", "English"])

if st.button("Generar clip viral"):
    if not youtube_url:
        st.warning("Por favor ingresa un link válido.")
    else:
        with st.spinner("Procesando video..."):
            audio_path, video_path = extract_youtube_audio(youtube_url)
            transcription = transcribe_audio(audio_path, language)
            segments = detect_viral_segments(transcription)
            caption = generate_captions(transcription, language)
            output_path = create_clip_with_subs(video_path, segments, transcription, caption, language)

        st.video(output_path)
        st.success("¡Clip generado!")
        st.download_button("Descargar clip", data=open(output_path, "rb"), file_name="clip_viral.mp4")
        st.markdown(f"**Caption sugerido:** {caption}")
