from flask import Flask, request
import os
from dotenv import load_dotenv
import sys

sys.stdout.reconfigure(encoding='utf-8')

# Load environment variables from .env
load_dotenv()

app = Flask(__name__)

@app.route("/")
def home():
    return "✅ AI Code Reviewer is Live (Week 5 - Mock Mode)!"

@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.json
    print("Webhook received!")

    repo_path = os.getcwd()  # Assuming you're running this from your project root
    commits = data.get("commits", [])
    
    for commit in commits:
        author = commit.get("author", {}).get("name", "Unknown")
        message = commit.get("message", "")
        modified_files = commit.get("modified", [])

        print(f"\nCommit by: {author}")
        print(f"Message: {message}")
        print("Files changed:")

        for file_path in modified_files:
            print(f"- {file_path}")
            full_path = os.path.join(repo_path, file_path)
            if os.path.exists(full_path) and file_path.endswith(('.py', '.js', '.html', '.css', '.txt')):
                try:
                    with open(full_path, "r", encoding="utf-8") as f:
                        code_content = f.read()

                    # 🔍 Mocked GPT Review
                    mocked_reply = (
                        f"🧠 (Mocked GPT Code Review for `{file_path}`)\n"
                        f"File contains {len(code_content.splitlines())} lines of code.\n"
                        "✅ Consider improving comments, adding exception handling, and ensuring code readability."
                    )
                    print(f"\n🔍 GPT Review for `{file_path}`:\n{mocked_reply}")
                except Exception as e:
                    print(f"⚠️ Error reading {file_path}: {e}")
            else:
                print(f"⚠️ Skipping unsupported or non-existent file: {file_path}")

    return {"status": "reviewed"}, 200

if __name__ == "__main__":
    app.run(port=5000)
#Krushna Chalwad