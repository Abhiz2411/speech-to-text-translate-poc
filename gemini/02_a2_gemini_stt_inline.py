import os
import time
from dotenv import load_dotenv
from google import genai
from google.genai import types

# -----------------------------------------------------
# 1. CONFIGURATION
# -----------------------------------------------------
TIMESTAMPED = False   # Set to False for non-timestamped transcription
AUDIO_FILE_PATH = r"data\2_Negative_Memories.mp3"
OUTPUT_DIR = r"output\transcribed\gemini"

# -----------------------------------------------------
# 2. START TIMER
# -----------------------------------------------------
start_time = time.time()

# -----------------------------------------------------
# 3. LOAD API KEY
# -----------------------------------------------------
load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if not GEMINI_API_KEY:
    raise ValueError("GEMINI_API_KEY not found in .env file")

# -----------------------------------------------------
# 4. INITIALIZE CLIENT
# -----------------------------------------------------
client = genai.Client(api_key=GEMINI_API_KEY)

# -----------------------------------------------------
# 5. READ AUDIO AS BYTES (inline mode)
# -----------------------------------------------------
print(f"Reading audio file as bytes: {AUDIO_FILE_PATH}")
with open(AUDIO_FILE_PATH, "rb") as f:
    audio_bytes = f.read()
print("Audio file loaded successfully (inline mode).")

# -----------------------------------------------------
# 6. BUILD PROMPT BASED ON VERSION FLAG
# -----------------------------------------------------
if TIMESTAMPED:
    print("\nUsing TIMESTAMPED transcription prompt...\n")
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
    output_file = os.path.join(OUTPUT_DIR, "gemini_stt_timestamped_inline.txt")
else:
    print("\nUsing NON-TIMESTAMPED transcription prompt...\n")
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
    output_file = os.path.join(OUTPUT_DIR, "gemini_stt_inline_flash.txt")

# -----------------------------------------------------
# 7. BUILD INLINE AUDIO PART
# -----------------------------------------------------
audio_part = types.Part.from_bytes(data=audio_bytes, mime_type="audio/mp3")

# -----------------------------------------------------
# 8. CALL GEMINI MODEL
# -----------------------------------------------------
print("Sending inline audio data to Gemini...\n")

response = client.models.generate_content(
    model="gemini-2.5-flash",  # Best for multilingual, code-mixed STT
    contents=[prompt, audio_part]
)

final_text = response.text or "(No transcription text returned)"

# -----------------------------------------------------
# 9. DISPLAY OUTPUT
# -----------------------------------------------------
print("\n================= GENERATED TRANSCRIPT =================\n")
print(final_text)
print("\n========================================================\n")

# -----------------------------------------------------
# 10. SAVE OUTPUT TO FILE
# -----------------------------------------------------
os.makedirs(os.path.dirname(output_file), exist_ok=True)
with open(output_file, "w", encoding="utf-8") as f:
    f.write(final_text)

print(f"✅ Transcript saved successfully at:\n{output_file}")

# -----------------------------------------------------
# 11. END TIMER AND LOG DURATION
# -----------------------------------------------------
end_time = time.time()
elapsed_time = end_time - start_time
minutes, seconds = divmod(elapsed_time, 60)
print(f"\nTotal processing time: {minutes:.0f} min {seconds:.2f} sec")
