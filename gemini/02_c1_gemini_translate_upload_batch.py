import os
import json
import time
from dotenv import load_dotenv
from google import genai

# -------------------------------------------------------------
# 1. CONFIGURATION
# -------------------------------------------------------------
AUDIO_PATH = r"data\2_Negative_Memories.mp3"  # Single audio or replace with loop for multiple
OUTPUT_DIR = r"output\translated\gemini\gemini_batch"
MODEL = "gemini-2.5-flash"
PROMPT = (
    "Translate this audio clip into English. "
    "The speaker may use Hindi, Gujarati, or both. "
    "Do not transcribe; only provide the English translation. "
    "Preserve tone and meaning accurately with correct grammar."
)
os.makedirs(OUTPUT_DIR, exist_ok=True)
BATCH_FILE = os.path.join(OUTPUT_DIR, "batch_requests.json")

# -------------------------------------------------------------
# 2. INITIALIZATION
# -------------------------------------------------------------
load_dotenv()
API_KEY = os.getenv("GEMINI_API_KEY")
if not API_KEY:
    raise ValueError("GEMINI_API_KEY not found in .env file")

client = genai.Client(api_key=API_KEY)

# -------------------------------------------------------------
# 3. UPLOAD AUDIO FILE
# -------------------------------------------------------------
print(f"Uploading audio: {AUDIO_PATH}")
music_file = client.files.upload(file=AUDIO_PATH)
print(f"Uploaded: {music_file.name} | MIME: {music_file.mime_type}")

# -------------------------------------------------------------
# 4. CREATE JSONL REQUEST FILE
# -------------------------------------------------------------
requests_data = [
    {
        "key": "translation_request",
        "request": {
            "contents": [
                {
                    "parts": [
                        {"text": PROMPT},
                        {
                            "file_data": {
                                "file_uri": music_file.uri,
                                "mime_type": music_file.mime_type,
                            }
                        },
                    ]
                }
            ]
        },
    }
]

print(f"Creating batch JSONL file: {BATCH_FILE}")
with open(BATCH_FILE, "w", encoding="utf-8") as f:
    for req in requests_data:
        f.write(json.dumps(req) + "\n")

# -------------------------------------------------------------
# 5. UPLOAD JSONL TO FILES API
# -------------------------------------------------------------
print("Uploading JSONL batch file...")
uploaded_batch_file = client.files.upload(file=BATCH_FILE)
print(f"Batch file uploaded: {uploaded_batch_file.name}")

# -------------------------------------------------------------
# 6. CREATE BATCH JOB
# -------------------------------------------------------------
print("Creating batch translation job...")
batch_job = client.batches.create(
    model=MODEL,
    src=uploaded_batch_file.name,
    config={"display_name": "audio-translation-batch"},
)
print(f"Job created: {batch_job.name}")

# -------------------------------------------------------------
# 7. POLL UNTIL COMPLETED
# -------------------------------------------------------------
print("Waiting for translation to finish...")
while True:
    job = client.batches.get(name=batch_job.name)
    if job.state.name in (
        "JOB_STATE_SUCCEEDED",
        "JOB_STATE_FAILED",
        "JOB_STATE_CANCELLED",
    ):
        break
    print(f"  Current state: {job.state.name} ...")
    time.sleep(20)

if job.state.name != "JOB_STATE_SUCCEEDED":
    print(f"Job failed: {job.state.name}")
    exit(1)

print("Translation job completed successfully.")

# -------------------------------------------------------------
# 8. DOWNLOAD RESULTS
# -------------------------------------------------------------
result_file = job.dest.file_name
print(f"Downloading result file: {result_file}")

file_content_bytes = client.files.download(file=result_file)
file_content = file_content_bytes.decode("utf-8")

# -------------------------------------------------------------
# 9. PARSE TRANSLATION AND SAVE
# -------------------------------------------------------------
for line in file_content.splitlines():
    if not line.strip():
        continue

    parsed = json.loads(line)
    key = parsed.get("key", "translation")
    response = parsed.get("response", {})
    candidates = response.get("candidates", [])
    if not candidates:
        continue

    translation_text = (
        candidates[0]
        .get("content", {})
        .get("parts", [{}])[0]
        .get("text", "")
        .strip()
    )

    if translation_text:
        output_file = os.path.join(OUTPUT_DIR, f"{key}_output.txt")
        with open(output_file, "w", encoding="utf-8") as f:
            f.write(translation_text)
        print(f"Saved translation: {output_file}")
    else:
        print("No translation text found in response.")

# -------------------------------------------------------------
# 10. CLEANUP
# -------------------------------------------------------------
print("Cleaning up temporary batch files...")
client.files.delete(name=uploaded_batch_file.name)
print("Deleted batch JSONL file from Gemini storage.")
print("Done.")
