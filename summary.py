import openai
import whisper
import yt_dlp
import os
from dotenv import load_dotenv
import sys

openai.api_key = os.getenv('OPENAI_TOKEN')
model = whisper.load_model("base")

def generate_response(prompt):
        response = openai.Completion.create(
            engine="text-davinci-002",
            prompt=prompt,
            max_tokens=120,
            n=1,
            stop=None,
            temperature=0.5,
        )
        return response.choices[0].text.strip()

def summary(url):
    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'quiet': True,
        'outtmpl': 'audio.%(ext)s',
    }
    
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

    # Transcribe video with whisper
    text = model.transcribe("audio.mp3")
    textstr = text["text"]
    with open("transcript.txt", "w") as f:
        f.write(textstr)
        f.close()

    print(generate_response(f"I have a text I would like to analyze. Here it is ***** {textstr} ***** Can you summarize this?"))

if __name__ == "__main__":
    if len(sys.argv) < 2:
        url = input("Please provide a youtube url. \n")
        summary(url)
    else:
        url = sys.argv[1]
        summary(url)