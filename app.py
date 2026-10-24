
import asyncio
import base64
import os
import uuid

import edge_tts
from deep_translator import GoogleTranslator, MyMemoryTranslator
from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from pydantic import BaseModel

app = FastAPI(title="BoloBridge API")


class TranslationRequest(BaseModel):
    text: str
    direction: str


def translate_text(text: str, direction: str) -> str:
    if direction == "ur-en":
        source, target = "urdu", "english"
    elif direction == "en-ur":
        source, target = "english", "urdu"
    else:
        raise ValueError("Direction must be ur-en or en-ur")

    try:
        result = GoogleTranslator(
            source=source,
            target=target
        ).translate(text)

        if result:
            return result

    except Exception as error:
        print("Google Translator failed:", error)

    try:
        result = MyMemoryTranslator(
            source=source,
            target=target
        ).translate(text)

        if result:
            return result

        raise ValueError("Translation returned empty text")

    except Exception as error:
        raise RuntimeError(
            f"Both translation services failed: {error}"
        )


async def create_audio(text: str, direction: str, filename: str):
    if direction == "ur-en":
        voice = "en-US-AriaNeural"
    else:
        voice = "ur-PK-UzmaNeural"

    communicator = edge_tts.Communicate(text, voice)
    await communicator.save(filename)


@app.get("/")
def home():
    html_path = os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        "index.html"
    )

    if not os.path.isfile(html_path):
        raise HTTPException(
            status_code=404,
            detail="index.html file was not found."
        )

    return FileResponse(html_path, media_type="text/html")


@app.post("/translate")
async def translate(request: TranslationRequest):
    text = request.text.strip()
    direction = request.direction

    if not text:
        raise HTTPException(
            status_code=400,
            detail="Please provide some text."
        )

    if direction not in ("ur-en", "en-ur"):
        raise HTTPException(
            status_code=400,
            detail="Direction must be ur-en or en-ur."
        )

    filename = os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        f"audio_{uuid.uuid4().hex}.mp3"
    )

    try:
        translated_text = await asyncio.to_thread(
            translate_text, text, direction
        )

        await create_audio(
            translated_text, direction, filename
        )

        with open(filename, "rb") as audio_file:
            audio_base64 = base64.b64encode(
                audio_file.read()
            ).decode("utf-8")

        return {
            "translated_text": translated_text,
            "audio_mp3": audio_base64
        }

    except Exception as error:
        print("BoloBridge error:", repr(error))
        raise HTTPException(
            status_code=502,
            detail=f"Translation or audio failed: {error}"
        )

    finally:
        if os.path.exists(filename):
            os.remove(filename)
