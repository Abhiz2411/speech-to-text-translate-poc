from google import genai
import os
from dotenv import load_dotenv

load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if not GEMINI_API_KEY:
    raise ValueError("GEMINI_API_KEY not found in .env file")

client = genai.Client(api_key=GEMINI_API_KEY)

audio_file_path = r"data\2_Negative_Memories.mp3"
print(f"Uploading audio file: {audio_file_path}")

myfile = client.files.upload(file=audio_file_path)
print(f"Upload complete. File ID: {myfile.name}")

client = genai.Client()
response = client.models.count_tokens(
  model='gemini-2.5-flash',
  contents=[
        (
            "Transcribe the spoken words exactly as heard. "
            "Preserve the original languages used (Hindi, Gujarati, or mixed). "
            "Do not translate — only transcribe the speech accurately."
        ),
        myfile
    ]
)

print(response)