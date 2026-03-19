import os
from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from openai import OpenAI

# Create app
app = FastAPI()

# Enable CORS (VERY IMPORTANT)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# OpenAI client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Home route
@app.get("/")
def home():
    return {"message": "Backend is running successfully 🚀"}

# Upload API
@app.post("/upload")
async def upload(file: UploadFile = File(...)):
    try:
        contents = await file.read()

        # Save file temporarily
        with open("temp_audio.webm", "wb") as f:
            f.write(contents)

        # Convert speech to text
        with open("temp_audio.webm", "rb") as f:
            transcript = client.audio.transcriptions.create(
                model="whisper-1",
                file=f
            )

        # Generate summary
        result = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{
                "role": "user",
                "content": f"""
                Summarize this meeting.
                Give:
                - Summary
                - Action items
                - Key decisions

                {transcript.text}
                """
            }]
        )

        return {"result": result.choices[0].message.content}

    except Exception as e:
        return {"error": str(e)}