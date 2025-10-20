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
output_dir = Path(r"C:\Users\Abhijit\Matrix\Work\Jio_Institute\Internship_PureBillion\STT-and-Translate-POC\output\transcribed\02_a1_stt_batch_R4.txt")
output_dir.mkdir(exist_ok=True)

def run_stt_sync():
    client = SarvamAI(api_subscription_key=SARVAM_API_KEY)
    job = client.speech_to_text_job.create_job(
        model="saarika:v2.5",
        with_diarization=False,
        with_timestamps=True,
        language_code="hi-IN",
        num_speakers=1,
    )
    print(f"Job created: {job._job_id}")
    job.upload_files(file_paths=audio_files, timeout=120.0)
    job.start()
    print("Transcription started...")
    job.wait_until_complete(poll_interval=5, timeout=60)
    
    if job.is_failed():
        raise RuntimeError("Transcription failed")
    
    job.download_outputs(output_dir=str(output_dir))
    print(f"Transcription completed. Output saved to: {output_dir}")

run_stt_sync()

# End timing
end_time = time.time()
elapsed_time = end_time - start_time
minutes, seconds = divmod(elapsed_time, 60)

print(f"\nTotal transcription time: {minutes:.0f} min {seconds:.2f} sec")