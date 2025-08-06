from flask import Flask, request
import os
from dotenv import load_dotenv
import sys

# Fix Unicode error in Windows terminal
sys.stdout.reconfigure(encoding='utf-8')

# Load environment variables from .env
load_dotenv()

app = Flask(__name__)

@app.route("/")
def home():
    return "✅ AI Code Reviewer is Live (Mock Mode)!"

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

            # Try reading the actual modified file content
            try:
                with open(file, "r", encoding="utf-8") as f:
                    code = f.read()

                # Mocked review for real code
                print(f"\n🔍 GPT Review for `{file}`:")
                print("🧠 (Mocked GPT Review)")
                print("✅ The structure looks fine. Consider adding docstrings and handling exceptions where necessary.\n")

            except Exception as e:
                print(f"⚠️ Could not read file `{file}`:", e)

    return {"status": "code-reviewed"}, 200

if __name__ == "__main__":
    app.run(port=5000)
