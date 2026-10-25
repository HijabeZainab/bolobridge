# BoloBridge

A web app for live voice translation between Urdu and English. Speak in one language, then read and hear the translation in the other.

## Features

- **Two-way translation:** Urdu to English and English to Urdu.
- **Spoken output:** the translated text is converted to natural-sounding speech (MP3) and played back.
- **Backup translator:** if Google Translate fails, the app automatically switches to MyMemory, so it keeps working.
- **Clean error handling:** empty text and wrong directions are rejected with clear messages.

## How it works

1. The user speaks or types text and picks a direction (`ur-en` or `en-ur`).
2. The browser sends the text to the `/translate` API.
3. The backend translates the text.
4. The translated text is turned into speech with Microsoft Edge neural voices.
5. The API returns the translated text and the audio, and the page shows and plays them.

## Tech stack

- Python and FastAPI (backend API)
- deep-translator (Google Translate, with MyMemory as backup)
- edge-tts (text-to-speech)
- HTML (frontend)

## API

`POST /translate`

Request:
`{ "text": "Hello", "direction": "en-ur" }`

Response:
`{ "translated_text": "...", "audio_mp3": "<base64 audio>" }`

## Run locally

1. Clone the repository:
   `git clone https://github.com/HijabeZainab/bolobridge.git`
2. Install the requirements:
   `pip install fastapi uvicorn edge-tts deep-translator`
3. Start the server:
   `uvicorn main:app --reload`
4. Open `http://127.0.0.1:8000` in your browser.

## Note

Translation and speech need an internet connection.

## Author

Hijab e Zainab, Data Science student
