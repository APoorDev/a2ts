import openai
import yt_dlp
import os
from dotenv import load_dotenv
import sys
import spacy
from spacy.lang.en import English

openai.api_key = os.getenv('OPENAI_TOKEN')
nlp = spacy.load("en_core_web_sm")
load_dotenv()

def let_user_pick(options):
    print("Please choose:")

    for idx, element in enumerate(options):
        print("{}) {}".format(idx + 1, element))

    i = input("Enter number: ")
    try:
        if 0 < int(i) <= len(options):
            return int(i) - 1
    except:
        pass
    return None


def text_to_chunks(text):
    chunks = [[]]
    chunk_total_words = 0

    sentences = nlp(text)

    for sentence in sentences.sents:
        chunk_total_words += len(sentence.text.split(" "))

        if chunk_total_words > 2700:
            chunks.append([])
            chunk_total_words = len(sentence.text.split(" "))

        chunks[len(chunks)-1].append(sentence.text)

    return chunks


def generate_response(textstr, typ):
    if typ == "podcast":
        prompt = f"I have a podcast I would like to analyze. Here is the transcript ***** {textstr} ***** Can you summarize this without mentioning that its a transcript?"
    elif typ == "lecture":
        prompt = f"I have a video lecture I would like to analyze. Here is the transcript ***** {textstr} ***** Can you summarize this without mentioning that its a transcript?"
    elif typ == "review":
        prompt = f"I have a video review I would like to analyze. Here is the transcript ***** {textstr} ***** Can you summarize this without mentioning that its a transcript?"
    else:
        prompt = f"I have a video transcript I would like to analyze. Here it is ***** {textstr} ***** Can you summarize this without mentioning that its a transcript?"
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        temperature=0.3,
        max_tokens=150,  # = 112 words
        top_p=1,
        frequency_penalty=0,
        presence_penalty=1
    )
    return response["choices"][0]["text"]


def summary(url, typ):
    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'outtmpl': 'audio.%(ext)s',
    }

    print("Downloading audio...")
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

    # Transcribe video with whisper
    print("Transcribing audio with whisper...")
    audio_file = open("audio.mp3", "rb")
    text = openai.Audio.transcribe("whisper-1",audio_file)
    audio_file.close()
    textstr = text["text"]
    with open("transcript.txt", "w") as f:
        f.write(textstr)
        f.close()
    print("Getting summary from ChatGPT...")
    chunk_summaries = []
    chunks = text_to_chunks(textstr)
    for chunk in chunks:
        chunk_summary = generate_response(" ".join(chunk), typ)
        chunk_summaries.append(chunk_summary)
    with open("summary.txt", "w") as f:
        f.write(" ".join(chunk_summaries))
        f.close()
    print(" ".join(chunk_summaries))

if __name__ == "__main__":
    if len(sys.argv) < 3:
        url = input("Please provide a youtube url. \n")
        print("You also need to provide the type of video. ")
        options = ['podcast', 'lecture', 'review', 'other']
        typ = let_user_pick(options)

        summary(url, typ)
    else:
        url = sys.argv[1]
        typ = sys.argv[2]
        summary(url, typ)
