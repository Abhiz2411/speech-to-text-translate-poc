import os
import json
import time
from dotenv import load_dotenv
from google import genai
from google.genai import types

# -------------------------------------------------------------
# 1. CONFIGURATION
# -------------------------------------------------------------
INPUT_DIR = r"data"
OUTPUT_DIR = r"output\translated\gemini_batch"
MODEL = "gemini-2.5-flash"
PROMPT = (
    "Translate this audio clip into English. "
    "The speaker may use Hindi, Gujarati, or both. "
    "Do not transcribe; only provide the English translation. "
    "Preserve tone and meaning accurately with correct grammar."
)
os.makedirs(OUTPUT_DIR, exist_ok=True)
BATCH_INPUT_FILE = os.path.join(OUTPUT_DIR, "batch_translation_input.jsonl")

# -------------------------------------------------------------
# 2. LOAD API KEY
# -------------------------------------------------------------
load_dotenv()
API_KEY = os.getenv("GEMINI_API_KEY")
if not API_KEY:
    raise ValueError("❌ GEMINI_API_KEY not found in .env file")

client = genai.Client(api_key=API_KEY)

# -------------------------------------------------------------
# 3. CREATE NDJSON FILE WITH INLINE REQUESTS
# -------------------------------------------------------------
print("📄 Creating batch input JSONL file...")
with open(BATCH_INPUT_FILE, "w", encoding="utf-8") as f:
    for filename in os.listdir(INPUT_DIR):
        if not filename.lower().endswith((".mp3", ".wav")):
            continue

        audio_path = os.path.join(INPUT_DIR, filename)
        print(f"📦 Adding {filename} to batch queue...")

        # Upload the audio file
        uploaded_audio = client.files.upload(file=audio_path)

        # Build the inlined request structure
        # req = {
        #     "inlined_request": {
        #         "contents": [
        #             {
        #                 "role": "user",
        #                 "parts": [
        #                     {"text": PROMPT},
        #                     {
        #                         "fileData": {
        #                             "mimeType": "audio/mp3",
        #                             "fileUri": uploaded_audio.uri
        #                         }
        #                     }
        #                 ]
        #             }
        #         ]
        #     }
        # }
        req = [
            {
                "contents": [
                    {
                        "role": "user",
                        'parts':[
                            {"text": PROMPT},
                            {
                               "fileData": {
                                    "mimeType": "audio/mp3",
                                    "fileUri": uploaded_audio.uri
                                }     
                            }]
                    }
                ]
            }
        ]

        f.write(json.dumps(req) + "\n")

print(f"✅ Batch input JSONL file created at: {BATCH_INPUT_FILE}")

# -------------------------------------------------------------
# 4. UPLOAD JSONL TO GEMINI FILES API
# -------------------------------------------------------------
print("\n📤 Uploading JSONL batch file to Gemini Files API...")

uploaded_batch_file = client.files.upload(
    file=BATCH_INPUT_FILE,
    # config={
    #     "mime_type": "application/jsonl",
    #     "display_name": "Batch Translation Input"
    # }
    config=types.UploadFileConfig(display_name=BATCH_INPUT_FILE, mime_type='jsonl')
)
print(f"✅ Uploaded batch file: {uploaded_batch_file.name}")

# -------------------------------------------------------------
# 5. CREATE BATCH JOB
# -------------------------------------------------------------
print("\n🚀 Submitting batch translation job to Gemini...")

batch_job = client.batches.create(
    model=MODEL,
    src=uploaded_batch_file.name
)
print(f"🆔 Batch job created: {batch_job.name}")

# -------------------------------------------------------------
# 6. POLL UNTIL COMPLETE
# -------------------------------------------------------------
print("\n⏳ Waiting for batch job to complete...")
while True:
    job = client.batches.get(name=batch_job.name)
    print(f"Current state: {job.state}")
    if job.state in ["SUCCEEDED", "FAILED", "CANCELLED"]:
        break
    time.sleep(15)

# -------------------------------------------------------------
# 7. FETCH RESULTS
# -------------------------------------------------------------
if job.state == "SUCCEEDED":
    print("\n✅ Batch translation completed successfully!")
    results = client.batches.get_results(name=batch_job.name)

    all_results_path = os.path.join(OUTPUT_DIR, "batch_translation_results.jsonl")
    with open(all_results_path, "w", encoding="utf-8") as f:
        for res in results:
            f.write(json.dumps(res, ensure_ascii=False) + "\n")

    print(f"📂 All raw results saved at: {all_results_path}")

    # Save each translation separately
    print("\n📝 Saving individual translations...")
    for idx, res in enumerate(results, 1):
        try:
            text = res.get("output", [{}])[0].get("content", "")
            if text:
                out_path = os.path.join(OUTPUT_DIR, f"translation_{idx}.txt")
                with open(out_path, "w", encoding="utf-8") as t:
                    t.write(text)
                print(f"✅ Saved: {out_path}")
        except Exception as e:
            print(f"⚠️ Error parsing result #{idx}: {e}")

else:
    print(f"❌ Batch job failed. Final state: {job.state}")

# -------------------------------------------------------------
# 8. CLEANUP
# -------------------------------------------------------------
print("\n🧹 Cleaning up uploaded batch file...")
client.files.delete(name=uploaded_batch_file.name)
print(f"🗑️ Deleted batch input file: {uploaded_batch_file.name}")

print("\n🎉 Batch translation workflow completed successfully.")
