import os
import time
from dotenv import load_dotenv
from google import genai

# -----------------------------------------------------
# 1. CONFIGURATION
# -----------------------------------------------------
AUDIO_FILE_PATH = r"data\2_Negative_Memories.mp3"
OUTPUT_DIR = r"output\translated\gemini"
MODEL_NAME = "gemini-2.5-pro"  # better multilingual understanding
TARGET_LANGUAGE = "English"

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
print(f"Uploading audio file for translation: {AUDIO_FILE_PATH}")
myfile = client.files.upload(file=AUDIO_FILE_PATH)
print(f"Upload complete. File ID: {myfile.name}")

# -----------------------------------------------------
# 6. TRANSLATION PROMPT
# -----------------------------------------------------
prompt = (
    "You are a professional speech translation assistant.\n"
    "Listen to the given audio clip carefully and translate everything spoken "
    "into clear, natural English.\n\n"
    "The speaker may use Hindi, Gujarati, or a mix of both.\n"
    "Do not provide the transcription in the original language—only output "
    "the English translation.\n"
    "Maintain the tone and meaning accurately, and ensure proper grammar and "
    "punctuation in English.\n"
)

# -----------------------------------------------------
# 7. GENERATE TRANSLATION
# -----------------------------------------------------
print("Translating audio to English... please wait.\n")

response = client.models.generate_content(
    model=MODEL_NAME,
    contents=[prompt, myfile]
)

final_text = response.text or "(No translation text returned)"

# -----------------------------------------------------
# 8. DISPLAY OUTPUT
# -----------------------------------------------------
print("\n================= TRANSLATED OUTPUT =================\n")
print(final_text)
print("\n=====================================================\n")

# -----------------------------------------------------
# 9. SAVE OUTPUT TO FILE
# -----------------------------------------------------
os.makedirs(OUTPUT_DIR, exist_ok=True)
output_file = os.path.join(OUTPUT_DIR, "gemini_translation_upload_pro.txt")
with open(output_file, "w", encoding="utf-8") as f:
    f.write(final_text)

print(f"English translation saved successfully at:\n{output_file}")

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
