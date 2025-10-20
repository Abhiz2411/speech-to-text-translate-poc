from sarvamai import SarvamAI
import os
import subprocess
import time
from pathlib import Path
from dotenv import load_dotenv
# Load environment variables from .env file
load_dotenv()

# Retrieve API key
SARVAM_API_KEY = os.getenv("SARVAM_API_KEY")

# Validate
if not SARVAM_API_KEY:
    raise ValueError("SARVAM_API_KEY not found. Please set it in your .env file.")

# Start timing before transcription
start_time = time.time()

client = SarvamAI(api_subscription_key=SARVAM_API_KEY)

audio_files = [r"C:\Users\Abhijit\Matrix\Work\Jio_Institute\Internship_PureBillion\STT-and-Translate-POC\data\2_Negative_Memories.mp3"]  # Update with your file path
output_dir = Path(r"output\translated\02_a2_sarvam_stt_translate_batch_R1.txt")
output_dir.mkdir(exist_ok=True)

def run_sttt_sync():
    client = SarvamAI(api_subscription_key=SARVAM_API_KEY)

    job = client.speech_to_text_translate_job.create_job(
        model="saaras:v2.5",
        with_diarization=False
        # num_speakers=1,
        # prompt="Official meeting"
    )

    print(f"Job created: {job._job_id}")
    job.upload_files(file_paths=audio_files, timeout=120.0)
    job.start()
    print("Translation started...")
    job.wait_until_complete(poll_interval=5, timeout=60)

    if job.is_failed():
        raise RuntimeError("Translation failed")

    job.download_outputs(output_dir=str(output_dir))
    print(f"Translation completed. Output saved to: {output_dir}")

run_sttt_sync()

# End timing
end_time = time.time()
elapsed_time = end_time - start_time
minutes, seconds = divmod(elapsed_time, 60)

print(f"\nTotal transcription time: {minutes:.0f} min {seconds:.2f} sec")