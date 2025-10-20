from sarvamai import SarvamAI
import os
import subprocess
import time
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

def file_format_check(audio_file_path):
    supported_formats = ['.wav', '.mp3']
    ext = os.path.splitext(audio_file_path)[1].lower()
    if ext not in supported_formats:
            print(f"Unsupported file format '{ext}'. Please upload a WAV or MP3 file.")
            return False
    print(f"File '{audio_file_path}' supported!")
    return True

def split_audio_ffmpeg(audio_path, chunk_duration=29, output_dir=r"output\chunked\stt_chunked"):
    os.makedirs(output_dir, exist_ok=True)
    ext = os.path.splitext(audio_path)[1].lower()
    base_name = os.path.splitext(os.path.basename(audio_path))[0]
    output_pattern = os.path.join(output_dir, f"{base_name}_%03d{ext}")
    codec = "pcm_s16le" if ext == ".wav" else "libmp3lame"
    command = [
        "ffmpeg",
        "-i", audio_path,
        "-f", "segment",
        "-segment_time", str(chunk_duration),
        "-c:a", codec,
        output_pattern
    ]
    print("Running command:", " ".join(command))
    result = subprocess.run(command, capture_output=True, text=True)
    print("Return code:", result.returncode)
    print("STDOUT:\n", result.stdout)
    print("STDERR:\n", result.stderr)
    output_files = sorted([
        os.path.join(output_dir, f) for f in os.listdir(output_dir)
        if f.endswith(ext)
    ])
    print("Chunks generated:", output_files)
    return output_files


# language_code="hi-IN" for Manually tagging Hindi, language_code="gu-IN" for Gujarati
# language_code="unknown" for Auto detection
# No language_code parametet for Code Mixed Speech
# def transcribe_audio_chunks_sdk(chunk_paths, client, model="saarika:v2.5", language_code="hi-IN"):
    
#     full_transcript = []

#     for idx, chunk_path in enumerate(chunk_paths):
#         print(f"\nTranscribing chunk {idx + 1}/{len(chunk_paths)} → {chunk_path}")
#         with open(chunk_path, "rb") as audio_file:
#             try:
#                 response = client.speech_to_text.transcribe(
#                     file=audio_file,
#                     model=model,
#                     language_code=language_code
#                 )
#                 print("Chunk Response:", response)
#                 full_transcript.append(str(response))
#             except Exception as e:
#                 print(f"Error with chunk {chunk_path}: {e}")

#     return " ".join(full_transcript).strip()

def transcribe_audio_chunks_sdk(chunk_paths, client, model="saarika:v2.5"):
    
    full_transcript = []

    for idx, chunk_path in enumerate(chunk_paths):
        print(f"\nTranscribing chunk {idx + 1}/{len(chunk_paths)} → {chunk_path}")
        with open(chunk_path, "rb") as audio_file:
            try:
                response = client.speech_to_text.transcribe(
                    file=audio_file,
                    model=model
                )
                print("Chunk Response:", response)
                full_transcript.append(str(response))
            except Exception as e:
                print(f"Error with chunk {chunk_path}: {e}")

    return " ".join(full_transcript).strip()


audio_file_path = r"C:\Users\Abhijit\Matrix\Work\Jio_Institute\Internship_PureBillion\STT-and-Translate-POC\data\2_Negative_Memories.mp3"
if file_format_check(audio_file_path):
    chunks = split_audio_ffmpeg(audio_path=audio_file_path)
    print("Data chunked successfully!")
    # 2. Transcribe each chunk and collate
    if chunks:
        final_transcript = transcribe_audio_chunks_sdk(chunks, client)
        print("\nFinal Combined Transcript:\n")
        print(final_transcript)
        # Define output path
        output_path = r"C:\Users\Abhijit\Matrix\Work\Jio_Institute\Internship_PureBillion\STT-and-Translate-POC\output\transcribed\01_a1_stt_transcribed_R3.txt"

        # Ensure directory exists
        os.makedirs(os.path.dirname(output_path), exist_ok=True)

        # Save transcript to file
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(final_transcript)

        print(f"\nTranscript saved at:\n{output_path}")
    else:
        print("No audio chunks generated. Transcription aborted.")

# End timing
end_time = time.time()
elapsed_time = end_time - start_time
minutes, seconds = divmod(elapsed_time, 60)

print(f"\nTotal transcription time: {minutes:.0f} min {seconds:.2f} sec")