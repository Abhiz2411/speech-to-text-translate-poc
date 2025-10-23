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
music_path = r'data\2_Negative_Memories.mp3'
OUTPUT_DIR = r"output\translated\gemini_batch"
MODEL = "gemini-2.5-flash"
PROMPT = (
    "Translate this audio clip into English. "
    "The speaker may use Hindi, Gujarati, or both. "
    "Do not transcribe; only provide the English translation. "
    "Preserve tone and meaning accurately with correct grammar."
)

load_dotenv()
API_KEY = os.getenv("GEMINI_API_KEY")
if not API_KEY:
    raise ValueError("❌ GEMINI_API_KEY not found in .env file")

client = genai.Client(api_key=API_KEY)

print(f"Uploading music file: {music_path}")
music_file = client.files.upload(
    file=music_path,
)
print(f"Uploaded music file: {music_file.name} with MIME type: {music_file.mime_type}")

requests_data = [
    {"key": "request_1", "request": {"contents": [{"parts": [{"text": "Explain how AI works in a few words"}]}]}},
    {"key": "request_2_audio", "request": {"contents": [{"parts": [
        {"text": PROMPT},
        {"file_data":{"file_uri": music_file.uri, "mime_type": music_file.mime_type}}
        ]}]}}
]

json_file_path = r'output\translated\gemini_batch_self\batch_requests.json'

print(f"\nCreating JSONL file: {json_file_path}")
with open(json_file_path, 'w') as f:
    for req in requests_data:
        f.write(json.dumps(req) + '\n')

# 2. Upload JSONL file to File API.
print(f"Uploading file: {json_file_path}")
uploaded_batch_requests = client.files.upload(
    file=json_file_path,
    # config=types.UploadFileConfig(display_name='batch-input-file')
)
print(f"Uploaded file: {uploaded_batch_requests.name}")

print("\nCreating batch job...")
batch_job_from_file = client.batches.create(
    model=MODEL,
    src=uploaded_batch_requests.name,
    config={
        'display_name': 'my-batch-job-from-file',
    }
)
print(f"Created batch job from file: {batch_job_from_file.name}")

# Note: You can check the status of any job by replacing its name here.
# For example: job_name = 'batches/your-job-name-here'

import time

job_name = batch_job_from_file.name

print(f"Polling status for job: {job_name}")

# Poll the job status until it's completed.
while True:
    batch_job = client.batches.get(name=job_name)
    if batch_job.state.name in ('JOB_STATE_SUCCEEDED', 'JOB_STATE_FAILED', 'JOB_STATE_CANCELLED'):
        break
    print(f"Job not finished. Current state: {batch_job.state.name}. Waiting 30 seconds...")
    time.sleep(30)

print(f"Job finished with state: {batch_job.state.name}")
if batch_job.state.name == 'JOB_STATE_FAILED':
    print(f"Error: {batch_job.error}")

# Retrieve and parse results
if batch_job.state.name == 'JOB_STATE_SUCCEEDED':
    # The output is in another file.
    result_file_name = batch_job.dest.file_name
    print(f"Results are in file: {result_file_name}")

    print("\nDownloading and parsing result file content...")
    file_content_bytes = client.files.download(file=result_file_name)
    file_content = file_content_bytes.decode('utf-8')

    # The result file is also a JSONL file. Parse and print each line.
    for line in file_content.splitlines():
      if line:
        parsed_response = json.loads(line)
        # Pretty-print the JSON for readability
        print(json.dumps(parsed_response, indent=2))
        print("-" * 20)
else:
    print(f"Job did not succeed. Final state: {batch_job.state.name}")