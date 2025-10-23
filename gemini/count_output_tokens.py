import tiktoken

# Path to your transcription file
file_path = r"output\translated\gemini\gemini_translation_upload_flash.txt"

# Choose a tokenizer model (e.g. GPT-4, GPT-3.5)
# For Gemini output, GPT-4 tokenizer will give a close approximation
encoding = tiktoken.encoding_for_model("gpt-4")

# Read the transcription text
with open(file_path, "r", encoding="utf-8") as f:
    text = f.read()

# Tokenize the text
tokens = encoding.encode(text)

# Count tokens
print(f"Total tokens: {len(tokens)}")
