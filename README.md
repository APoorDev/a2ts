# Audio 2 Text Summary
THIS BRANCH IS A WIP
This branch uses the [gpt4all](https://github.com/nomic-ai/gpt4all) a LLaMa based chatbot trained on GPT-3.5-Turbo Generations.

Use the api-only branch if you want to do everything over the openai api.

## Description
This is a python script that downloads the audio from any youtube video, transcripts it using whisper, and pipes it into [gpt4all](https://github.com/nomic-ai/gpt4all) to get a summary.

## Installation
Install requirements
```bash
pip install -r requirements.txt
python -m spacy download en_core_web_sm
```
## Usage
```bash
python3 ./summary.py [LINK]
```
or just
```bash
python3 ./summary.py
```