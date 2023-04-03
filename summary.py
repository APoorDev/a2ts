import whisper
from nomic.gpt4all import GPT4All
import yt_dlp
import sys
import spacy
from spacy.lang.en import English

model = whisper.load_model("base")
nlp = spacy.load("en_core_web_sm")

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


def generate_response(textstr):
    prompt = f"I would like you to analyze a piece of text. Here it is ***** {textstr} ****** Can you summarize this without an introduction in 112 words or less?"
    m = GPT4All()
    m.open()
    response = m.prompt(prompt)
    return response


def summary(url):
    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '50',
        }],
        'outtmpl': 'audio.%(ext)s',
    }

    print("Downloading audio...")
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

    # Transcribe video with whisper
    print("Transcribing audio with whisper...")
    text = model.transcribe("audio.mp3")
    textstr = text["text"]
    with open("transcript.txt", "w") as f:
        f.write(textstr)
        f.close()
    print("Getting summary from ChatGPT...")
    chunk_summaries = []
    chunks = text_to_chunks(textstr)
    for chunk in chunks:
        chunk_summary = generate_response(" ".join(chunk))
        chunk_summaries.append(chunk_summary)
    with open("summary.txt", "w") as f:
        f.write(" ".join(chunk_summaries))
        f.close()
    print(" ".join(chunk_summaries))

if __name__ == "__main__":
    if len(sys.argv) < 2:
        url = input("Please provide a youtube url. \n")
        summary(url)
    else:
        url = sys.argv[1]
        summary(url)
