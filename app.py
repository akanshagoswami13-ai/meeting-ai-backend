import os
from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from openai import OpenAI

app = FastAPI()

# CORS FIX
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

@app.get("/")
def home():
    return {"message": "Backend is running successfully 🚀"}

@app.post("/upload")
async def upload(file: UploadFile = File(...)):
    try:
        contents = await file.read()

        with open("temp_audio.webm", "wb") as f:
            f.write(contents)

        with open("temp_audio.webm", "rb") as f:
            transcript = client.audio.transcriptions.create(
                model="whisper-1",
                file=f
            )

        result = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{
                "role": "user",
                "content": f"""
                Create a clean meeting summary.

                Include:
                - Summary
                - Action items
                - Key decisions

                Transcript:
                {transcript.text}
                """
            }]
        )

        final_text = result.choices[0].message.content

        return {"result": final_text}

    except Exception as e:
        return {"result": f"Error: {str(e)}"}