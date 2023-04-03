# Audio 2 Text Summary
The main branch runs whisper locally which can use a lot of resources.

Use the api-only branch if you want to do everything over the openai api.

## Description
This is a python script that downloads the audio from any youtube video, transcripts it using whisper, and pipes it into ChatGPT to get a summary.

## Installation
Install requirements
```bash
pip install -r requirements.txt
python -m spacy download en_core_web_sm
```
You also need to set your API keys into a .env file. You can use the `.envexample` as a reference. 

## Usage
```bash
python3 ./summary.py [LINK]
```
or just
```bash
python3 ./summary.py
```