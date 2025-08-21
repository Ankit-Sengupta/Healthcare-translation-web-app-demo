import os, tempfile
from fastapi import FastAPI, Form
from fastapi.responses import JSONResponse, FileResponse
from gtts import gTTS
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],   
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/translate/")
async def translate_text(
    text: str = Form(...),
    input_lang_code: str = Form(...),
    output_lang_code: str = Form(...)
):
   
    translated_text = f"[{output_lang_code}] {text}"

   
    tts = gTTS(translated_text, lang=output_lang_code)
    temp_audio = tempfile.NamedTemporaryFile(delete=False, suffix=".mp3")
    tts.save(temp_audio.name)

    return JSONResponse({
        "original_text": text,
        "translated_text": translated_text,
        "audio_file": os.path.basename(temp_audio.name)
    })


@app.get("/audio/{filename}")
async def serve_audio(filename: str):
    path = os.path.join(tempfile.gettempdir(), filename)
    return FileResponse(path, media_type="audio/mpeg")


