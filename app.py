from flask import Flask, request
import os
from dotenv import load_dotenv
import sys

# Ensure UTF-8 encoding for emojis/logs
sys.stdout.reconfigure(encoding='utf-8')

# Load environment variables from .env
load_dotenv()

app = Flask(__name__)

@app.route("/")
def home():
    return "✅ AI Code Reviewer is Live (Mock Mode with Code Review)!"

@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.json
    print("Webhook received!")

    commits = data.get("commits", [])
    for commit in commits:
        author = commit.get("author", {}).get("name", "Unknown")
        message = commit.get("message", "")
        modified_files = commit.get("modified", [])

        print(f"Commit by: {author}")
        print(f"Message: {message}")
        print("Files changed:")
        
        for file in modified_files:
            print(f"- {file}")
            try:
                with open(file, "r", encoding="utf-8") as f:
                    code_content = f.read()
            except Exception as e:
                code_content = f"[⚠️ Error reading file: {e}]"

            # Simulate GPT code review
            mocked_code_review = (
                f"🧠 (Mocked GPT Code Review for `{file}`)\n"
                f"File contains {len(code_content.splitlines())} lines of code.\n"
                "✅ Consider improving comments, adding exception handling, and ensuring code readability."
            )
            print("\n🔍 GPT Review for `{}`:\n{}".format(file, mocked_code_review))

    return {"status": "reviewed"}, 200

if __name__ == "__main__":
    app.run(port=5000)
# 🔧 Week 4 test: Triggering mock code review with file content
