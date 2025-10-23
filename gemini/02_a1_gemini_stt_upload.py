import os
import time
from dotenv import load_dotenv
from google import genai

# -----------------------------------------------------
# 1. Start timer
# -----------------------------------------------------
start_time = time.time()

# -----------------------------------------------------
# 2. Load API Key from .env
# -----------------------------------------------------
load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if not GEMINI_API_KEY:
    raise ValueError("GEMINI_API_KEY not found in .env file")

# -----------------------------------------------------
# 3. Initialize Gemini client
# -----------------------------------------------------
client = genai.Client(api_key=GEMINI_API_KEY)

# -----------------------------------------------------
# 4. Upload the audio file
# -----------------------------------------------------
audio_file_path = r"data\2_Negative_Memories.mp3"
print(f"Uploading audio file: {audio_file_path}")

myfile = client.files.upload(file=audio_file_path)
print(f"Upload complete. File ID: {myfile.name}")

# -----------------------------------------------------
# 5. Transcribe with timestamps & language labels
# -----------------------------------------------------
print("\nPerforming multilingual (Hindi + Gujarati) transcription with timestamps...\n")

prompt = (
    "You are a professional multilingual transcription assistant.\n"
    "Transcribe the audio exactly as spoken, preserving both spoken language and script.\n"
    "Automatically detect when the speaker switches between Hindi and Gujarati.\n"
    "For Hindi speech, use the Devanagari script (e.g., नमस्ते, क्या हाल है?).\n"
    "For Gujarati speech, use the Gujarati script (e.g., કેમ છો?, તમારું સ્વાગત છે.).\n"
    "Do NOT transliterate or translate; use the native script of the detected language.\n\n"
    "Return the output in the following format:\n"
    "[start_time - end_time] (Language): transcribed text in correct native script\n\n"
    "Example:\n"
    "[00:00 - 00:12] (Hindi): नमस्ते, मेरा नाम अभिजीत है।\n"
    "[00:13 - 00:27] (Gujarati): હવે હું તમારું સ્વાગત કરું છું।"
)


response = client.models.generate_content(
    model="gemini-2.5-flash",  # use pro for better multilingual accuracy
    contents=[prompt, myfile]
)

final_text = response.text or "(No transcription text returned)"

# -----------------------------------------------------
# 6. Display and Save Output
# -----------------------------------------------------
print("\n================= TIMESTAMPED MULTILINGUAL TRANSCRIPT =================\n")
print(final_text)
print("\n=======================================================================\n")

output_path = r"output\transcribed\gemini\gemini_stt_upload_flash_timestamped_native_corrected.txt"
os.makedirs(os.path.dirname(output_path), exist_ok=True)
with open(output_path, "w", encoding="utf-8") as f:
    f.write(final_text)

print(f"Transcript saved successfully at:\n{output_path}")

# -----------------------------------------------------
# 7. Cleanup: Delete uploaded file to save storage
# -----------------------------------------------------
client.files.delete(name=myfile.name)
print(f"Temporary audio file deleted from Gemini servers: {myfile.name}")

# -----------------------------------------------------
# 8. End timer and log duration
# -----------------------------------------------------
end_time = time.time()
elapsed_time = end_time - start_time
minutes, seconds = divmod(elapsed_time, 60)
print(f"\nTotal processing time: {minutes:.0f} min {seconds:.2f} sec")
