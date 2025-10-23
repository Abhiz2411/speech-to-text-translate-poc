import os
import time
from dotenv import load_dotenv
from google import genai

# -----------------------------------------------------
# 1. CONFIGURATION
# -----------------------------------------------------
TIMESTAMPED = False   # Set this flag to False for non-timestamped version
AUDIO_FILE_PATH = r"data\2_Negative_Memories.mp3"
OUTPUT_DIR = r"output\transcribed\gemini"

# -----------------------------------------------------
# 2. START TIMER
# -----------------------------------------------------
start_time = time.time()

# -----------------------------------------------------
# 3. LOAD ENVIRONMENT VARIABLES
# -----------------------------------------------------
load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if not GEMINI_API_KEY:
    raise ValueError("GEMINI_API_KEY not found in .env file")

# -----------------------------------------------------
# 4. INITIALIZE GEMINI CLIENT
# -----------------------------------------------------
client = genai.Client(api_key=GEMINI_API_KEY)

# -----------------------------------------------------
# 5. UPLOAD AUDIO FILE
# -----------------------------------------------------
print(f"Uploading audio file: {AUDIO_FILE_PATH}")
myfile = client.files.upload(file=AUDIO_FILE_PATH)
print(f"Upload complete. File ID: {myfile.name}")

# -----------------------------------------------------
# 6. BUILD PROMPT BASED ON VERSION FLAG
# -----------------------------------------------------
if TIMESTAMPED:
    print("\n🧠 Using TIMESTAMPED transcription prompt...\n")
    prompt = (
        "You are a professional multilingual transcription assistant.\n"
        "Transcribe the audio exactly as spoken, preserving both spoken language and script.\n"
        "Automatically detect when the speaker switches between Hindi and Gujarati.\n"
        "For Hindi speech, use Devanagari script (e.g., नमस्ते, क्या हाल है?).\n"
        "For Gujarati speech, use Gujarati script (e.g., કેમ છો?, તમારું સ્વાગત છે.).\n"
        "Do NOT transliterate or translate; use the native script of each detected language.\n\n"
        "Return the output as a structured list with timestamps in this format:\n"
        "[start_time - end_time] (Language): transcribed text\n\n"
        "Example:\n"
        "[00:00 - 00:12] (Hindi): नमस्ते, मेरा नाम अभिजीत है।\n"
        "[00:13 - 00:27] (Gujarati): હવે હું તમારું સ્વાગત કરું છું।"
    )
    output_file = os.path.join(OUTPUT_DIR, "gemini_stt_upload_flash_timestamped_versioned.txt")

else:
    print("\n🧠 Using NON-TIMESTAMPED transcription prompt...\n")
    prompt = (
        "You are a professional multilingual transcription assistant.\n"
        "Transcribe the audio exactly as spoken, preserving both spoken language and script.\n"
        "Automatically detect when the speaker switches between Hindi and Gujarati.\n"
        "For Hindi speech, use Devanagari script (e.g., नमस्ते, क्या हाल है?).\n"
        "For Gujarati speech, use Gujarati script (e.g., કેમ છો?, તમારું સ્વાગત છે.).\n"
        "Do NOT transliterate or translate; use the native script of each detected language.\n\n"
        "Return the output as plain text transcription without timestamps.\n"
        "Maintain proper punctuation and spacing for readability."
    )
    output_file = os.path.join(OUTPUT_DIR, "gemini_stt_upload_pro_versioned.txt")

# -----------------------------------------------------
# 7. GENERATE CONTENT
# -----------------------------------------------------
print("🚀 Generating transcription...\n")
response = client.models.generate_content(
    model="gemini-2.5-pro",  # Better multilingual & code-mixed support
    contents=[prompt, myfile]
)

final_text = response.text or "(No transcription text returned)"

# -----------------------------------------------------
# 8. DISPLAY OUTPUT
# -----------------------------------------------------
print("\n================= GENERATED TRANSCRIPT =================\n")
print(final_text)
print("\n========================================================\n")

# -----------------------------------------------------
# 9. SAVE OUTPUT
# -----------------------------------------------------
os.makedirs(os.path.dirname(output_file), exist_ok=True)
with open(output_file, "w", encoding="utf-8") as f:
    f.write(final_text)

print(f"Transcript saved successfully at:\n{output_file}")

# -----------------------------------------------------
# 10. CLEANUP (DELETE TEMP FILE FROM GEMINI)
# -----------------------------------------------------
client.files.delete(name=myfile.name)
print(f"Temporary uploaded file deleted: {myfile.name}")

# -----------------------------------------------------
# 11. END TIMER
# -----------------------------------------------------
end_time = time.time()
elapsed_time = end_time - start_time
minutes, seconds = divmod(elapsed_time, 60)
print(f"\nTotal processing time: {minutes:.0f} min {seconds:.2f} sec")
