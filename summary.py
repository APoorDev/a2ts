import openai
import whisper
import pytube
import os

openai.api_key = os.getenv('OPENAI_TOKEN')
model = whisper.load_model("base")

def generate_response(self, prompt):
        response = openai.Completion.create(
            engine="text-davinci-002",
            prompt=prompt,
            max_tokens=120,
            n=1,
            stop=None,
            temperature=0.5,
        )
        return response.choices[0].text.strip()

video = "https://www.youtube.com/watch?v=x7X9w_GIm1s"
data = pytube.YouTube(video)

# Convert audio to mp4
audio = data.streams.get_audio_only()
audio.download(filename="audio.mp3")

# Transcribe video with whisper
text = model.transcribe()

generate_response(f"Could you provide a summary of the following? \n {text}")