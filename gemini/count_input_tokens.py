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
            "You are a professional speech translation assistant.\n"
            "Listen to the given audio clip carefully and translate everything spoken "
            "into clear, natural English.\n\n"
            "The speaker may use Hindi, Gujarati, or a mix of both.\n"
            "Do not provide the transcription in the original language—only output "
            "the English translation.\n"
            "Maintain the tone and meaning accurately, and ensure proper grammar and "
            "punctuation in English.\n"
        ),
        myfile
    ]
)

print(response)