from flask import Flask, request
import os
from dotenv import load_dotenv

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

        # Instead of GPT response, mock the review output
        mocked_reply = (
            "🧠 (Mocked GPT Review)\n"
            "Your commit message looks good overall. Consider making it more descriptive "
            "for better team collaboration."
        )
        print("\n🔍 GPT Review:\n", mocked_reply)

    return {"status": "reviewed"}, 200

if __name__ == "__main__":
    app.run(port=5000)
