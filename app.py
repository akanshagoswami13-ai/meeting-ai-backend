@app.get("/")
def home():
    return {"message": "Backend is running successfully 🚀"}
import os
from fastapi import FastAPI, UploadFile, File
from openai import OpenAI

app = FastAPI()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
@app.post("/upload")
async def upload(file: UploadFile = File(...)):
    audio = await file.read()

    # Step 1: Speech to text
    transcript = client.audio.transcriptions.create(
        model="whisper-1",
        file=audio
    )

    # Step 2: AI summary
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{
            "role": "user",
            "content": f"""
            Summarize this meeting and give actions:

            {transcript.text}
            """
        }]
    )

    return {"result": response.choices[0].message.content}