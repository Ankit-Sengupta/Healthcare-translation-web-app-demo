from fastapi import FastAPI, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from openai import OpenAI
import os
import tempfile

app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

@app.post("/translate/")
async def translate(
    text: str = Form(...),
    input_lang_code: str = Form(...),
    output_lang_code: str = Form(...)
):
    try:
      
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": f"You are a translator. Translate from {input_lang_code} to {output_lang_code}."},
                {"role": "user", "content": text}
            ]
        )
        translated_text = response.choices[0].message.content.strip()

     
        speech_file = tempfile.NamedTemporaryFile(delete=False, suffix=".mp3")
        with client.audio.speech.with_streaming_response.create(
            model="gpt-4o-mini-tts",
            voice="alloy",
            input=translated_text
        ) as response:
            response.stream_to_file(speech_file.name)

        audio_filename = os.path.basename(speech_file.name)

        return {
            "original_text": text,
            "translated_text": translated_text,
            "audio_file": audio_filename
        }

    except Exception as e:
        return {"error": str(e)}


@app.get("/audio/{filename}")
async def get_audio(filename: str):
    file_path = os.path.join(tempfile.gettempdir(), filename)
    if os.path.exists(file_path):
        return FileResponse(file_path, media_type="audio/mpeg")
    return {"error": "File not found"}

