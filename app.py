from flask import Flask, request
import os
import requests
from dotenv import load_dotenv
import sys

# Fix UTF-8 printing
sys.stdout.reconfigure(encoding='utf-8')

# Load .env variables
load_dotenv()

app = Flask(__name__)

# Hugging Face API settings
HUGGINGFACE_API_KEY = os.getenv("HUGGINGFACE_API_KEY")
HF_MODEL = "bigcode/starcoder"  # Good for code analysis

# Base repo path (directory where this script is located)
REPO_ROOT = os.path.dirname(os.path.abspath(__file__))


def hf_code_review(prompt):
    """Send prompt to Hugging Face Inference API and return response."""
    url = f"https://api-inference.huggingface.co/models/{HF_MODEL}"
    headers = {"Authorization": f"Bearer {HUGGINGFACE_API_KEY}"}
    payload = {"inputs": prompt}

    response = requests.post(url, headers=headers, json=payload)
    if response.status_code == 200:
        try:
            data = response.json()
            if isinstance(data, list) and len(data) > 0:
                return data[0].get("generated_text", "").strip()
            elif isinstance(data, dict) and "generated_text" in data:
                return data["generated_text"].strip()
        except Exception as e:
            return f"⚠️ Error parsing response: {e}"
    return f"⚠️ Error from Hugging Face API: {response.text}"


def is_text_file(filepath):
    """Check if file is a text file (skip binaries)."""
    try:
        with open(filepath, "rb") as f:
            chunk = f.read(1024)
            return b"\0" not in chunk  # Binary files usually contain null bytes
    except Exception:
        return False


def read_file_content(filepath):
    """Safely read file content if it exists."""
    try:
        file_path = os.path.join(REPO_ROOT, filepath)  # Full path
        if os.path.exists(file_path) and is_text_file(file_path):
            with open(file_path, "r", encoding="utf-8") as f:
                return f.read()
        else:
            print(f"⚠️ Skipping unsupported or missing file: {filepath}")
            return None
    except Exception as e:
        return f"⚠️ Error reading file: {e}"


@app.route("/")
def home():
    return "✅ AI Code Reviewer (Hugging Face, Full File Review) is Live!"


@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.json
    print("Webhook received!")

    commits = data.get("commits", [])
    for commit in commits:
        author = commit.get("author", {}).get("name", "Unknown")
        message = commit.get("message", "")
        modified_files = commit.get("modified", [])

        print(f"\nCommit by: {author}")
        print(f"Message: {message}")
        print("Files changed:")

        for file in modified_files:
            print(f"- {file}")
            file_content = read_file_content(file)

            if file_content:
                prompt = f"Review the following code and suggest improvements:\n\n{file_content}"
                review = hf_code_review(prompt)
                print(f"\n🔍 AI Review for `{file}`:\n{review}\n")
            else:
                print(f"⚠️ Skipping unsupported or missing file: {file}")

    return {"status": "reviewed"}, 200


if __name__ == "__main__":
    app.run(port=5000)
# test commit for webhook
