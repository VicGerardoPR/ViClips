import yt_dlp
from moviepy.editor import VideoFileClip, TextClip, CompositeVideoClip
import whisper
import os
from transformers import pipeline

def extract_youtube_audio(url):
    ydl_opts = {
        'format': 'bestvideo+bestaudio/best',
        'outtmpl': 'video.%(ext)s',
        'merge_output_format': 'mp4',
        'cookiefile': 'cookies.txt',  # si lo usas
        'quiet': True
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

    video_path = "video.mp4"
    audio_path = "audio.wav"
    VideoFileClip(video_path).audio.write_audiofile(audio_path)
    return audio_path, video_path

def transcribe_audio(audio_path, language):
    model = whisper.load_model("base")
    result = model.transcribe(audio_path, language="es" if language == "Español" else "en")
    return result["text"]

def detect_viral_segments(transcription):
    words = transcription.split()
    clip_segments = []
    for i in range(0, len(words), 30):
        clip_segments.append(" ".join(words[i:i+30]))
    return clip_segments[:1]  # tomar solo el primer segmento viral

def generate_captions(transcription, language):
    prompt = "Crea un caption viral estilo TikTok para este texto:\n" if language == "Español" else "Create a viral TikTok-style caption for this text:\n"
    return prompt + transcription[:150] + "..."

def create_clip_with_subs(video_path, segments, transcription, caption, language):
    clip = VideoFileClip(video_path).subclip(0, 15).resize(height=1080, width=608)
    subtitle_text = segments[0]
    txt_clip = TextClip(
        subtitle_text,
        fontsize=60,
        color='white',
        stroke_color='black',
        stroke_width=2,
        font='Arial-Bold',
        size=clip.size,
        method='caption'
    ).set_position(('center', 'bottom')).set_duration(clip.duration)

    final = CompositeVideoClip([clip, txt_clip])
    output_path = "outputs/clip_viral.mp4"
    os.makedirs("outputs", exist_ok=True)
    final.write_videofile(output_path, fps=24, codec='libx264')
    return output_path
