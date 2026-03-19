import os
from fastapi import FastAPI, UploadFile, File
from openai import OpenAI

# ✅ Create app FIRST
app = FastAPI()

# ✅ OpenAI client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# ✅ Home route
@app.get("/")
def home():
    return {"message": "Backend is running successfully 🚀"}

# ✅ Upload route
@app.post("/upload")
async def upload(file: UploadFile = File(...)):
    audio = await file.read()

    transcript = client.audio.transcriptions.create(
        model="whisper-1",
        file=audio
    )

    result = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{
            "role": "user",
            "content": f"Summarize this meeting:\n{transcript.text}"
        }]
    )

    return {"result": result.choices[0].message.content}
