import os
from yt_dlp import YoutubeDL

url = input("Cole o link do YouTube: ")

ffmpeg_path = os.path.join(os.getcwd(), "ffmpeg")

ydl_opts = {
    "format": "bestaudio/best",
    "postprocessors": [{
        "key": "FFmpegExtractAudio",
        "preferredcodec": "mp3",
        "preferredquality": "192",
    }],
    "ffmpeg_location": ffmpeg_path,
}

with YoutubeDL(ydl_opts) as ydl:
    ydl.download([url])

print("Download finalizado!")