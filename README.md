# 🎯 Proof of Concept: Speech-to-Text and Translation System

## 📘 Project Overview

This Proof of Concept (POC) project focuses on building a robust
**Speech-to-Text (STT)** and **Translation** system capable of handling
over **10,000 hours of multilingual video data**. The primary languages
involved are **Hindi** and **Gujarati**, with the target translation
language being **English**.

The goal is to evaluate multiple APIs for performance, cost, and
accuracy to determine the best-fit architecture for production
deployment.

------------------------------------------------------------------------

## 🚀 Getting Started

### Prerequisites

- **Python 3.11+** (required)
- **uv** package manager ([Install uv](https://docs.astral.sh/uv/))
- **ffmpeg** (for audio processing)
- API Keys for:
  - Sarvam AI
  - Google Gemini (optional)
  - OpenAI (optional)

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd STT-and-Translate-POC
   ```

2. **Install dependencies using uv**
   ```bash
   uv sync
   ```
   This will create a virtual environment and install all dependencies from `pyproject.toml`.

3. **Set up environment variables**

   Create a `.env` file in the project root with your API keys:
   ```bash
   SARVAM_API_KEY=your_sarvam_api_key_here
   GEMINI_API_KEY=your_gemini_api_key_here
   OPENAI_API_KEY=your_openai_api_key_here
   ```

4. **Install ffmpeg** (if not already installed)
   - **Ubuntu/Debian**: `sudo apt install ffmpeg`
   - **macOS**: `brew install ffmpeg`
   - **Windows**: Download from [ffmpeg.org](https://ffmpeg.org/download.html)

### Running the Scripts

Run any script using `uv run`:

```bash
# Sarvam AI - STT (Real-time chunked)
uv run sarvam/01_a1_sarvam_stt_realtime_chunked.py

# Sarvam AI - STT + Translation (Real-time chunked)
uv run sarvam/01_a2_sarvam_stt_translate_realtime_chunked.py

# Sarvam AI - STT (Batch)
uv run sarvam/02_a1_sarvam_stt_batch.py

# Sarvam AI - STT + Translation (Batch)
uv run sarvam/02_a2_sarvam_stt_translate_batch.py

# Google Gemini - STT
uv run gemini/02_gemini_stt.py

# Google Gemini - STT + Translation
uv run gemini/02_gemini_stt_translate.py

# OpenAI - STT
uv run openai/03_openai_stt.py

# OpenAI - STT + Translation
uv run openai/03_openai_stt_translate.py
```

**Note**: Update the audio file paths in each script to point to your input audio files in the `data/` directory.

------------------------------------------------------------------------

## 🧩 Objective

To compare and analyze three major APIs: 
- 1. **Sarvam AI**
- 2. **Google Gemini** 
- 3. **OpenAIWhisper / GPT** 

------------------------------------------------------------------------

## 🧠 Evaluation Metrics

  -----------------------------------------------------------------------
  Category                Metric              Description
  ----------------------- ------------------- ---------------------------
  **Speech-to-Text**      Word Error Rate     Measures transcription
                          (WER)               accuracy

                          Language Support    Support for Gujarati and
                                              Hindi

                          Speed               Real-time or batch
                                              performance

  **Translation**         BLEU / COMET Score  Translation quality from
                                              source to English

                          Context             Ability to retain meaning
                          Preservation        and tone

  **Cost**                API usage cost      Total cost per hour of
                                              audio

  **Ease of Integration** API flexibility     Ease of using SDKs and APIs

  **Scalability**         Throughput          Ability to handle large
                                              batch processing
  -----------------------------------------------------------------------

------------------------------------------------------------------------

## ⚙️ Proposed Architecture

               ┌────────────────────┐
               │     Video Data     │
               │ (10K+ Hours, mp4)  │
               └─────────┬──────────┘
                         │
               ┌─────────▼──────────┐
               │   Audio Extraction │
               │ (ffmpeg, mp3/wav)  │
               └─────────┬──────────┘
                         │
               ┌─────────▼──────────┐
               │   Speech to Text   │
               │ (Sarvam / Gemini / │
               │   OpenAI Whisper)  │
               └─────────┬──────────┘
                         │
               ┌─────────▼──────────┐
               │    Translation     │
               │ (Gemini / OpenAI)  │
               └─────────┬──────────┘
                         │
               ┌─────────▼──────────┐
               │   English Output   │
               │   (Text Storage)   │
               └────────────────────┘

------------------------------------------------------------------------

## 🧪 Experimental Setup

### Input Data

-   Format: `.mp3` extracted from sample video
-   Language: Hindi / Gujarati

### API Comparison Scripts

  -----------------------------------------------------------------------
  File Name                          Description
  ---------------------------------- ------------------------------------
  `sarvam_stt_test.py`               Performs STT using Sarvam API

  `gemini_translation_test.py`       Performs translation using Gemini
                                     API

  `openai_stt_translation_test.py`   Performs both STT + translation
                                     using OpenAI API
  -----------------------------------------------------------------------

Each script logs metrics such as transcription accuracy, translation
quality, and execution time.

------------------------------------------------------------------------

## 💰 Cost Tracking

To assess the economic feasibility: - Compute cost/hour for each API. -
Estimate total cost for 10K hours of video data.

------------------------------------------------------------------------

## 📊 Output Reports

Each experiment should output: 1. **STT Accuracy (WER %)**\
2. **Translation Accuracy (BLEU / COMET)**\
3. **Execution Time (s)**\
4. **Estimated Cost (per hr)**

These results will be summarized in a comparison report.

------------------------------------------------------------------------

## 🚀 Deliverables

1.  **Three standalone Python scripts** for API testing.
2.  **Comparison Report** in CSV/Markdown format.
3.  **Recommendation Summary** --- which API or hybrid approach is best.

------------------------------------------------------------------------

## 🧩 Future Scope

-   Incorporate automatic language detection.
-   Add video diarization for speaker separation.
-   Explore fine-tuning for domain-specific speech.

------------------------------------------------------------------------

## 👤 Author

**Abhijit Zende**\
AI Intern, PureBillion Technologies\
Date: October 2025
