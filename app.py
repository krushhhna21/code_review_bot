from flask import Flask, request
import os
from dotenv import load_dotenv
import openai

# Load environment variables from .env
load_dotenv()

# Set up OpenAI client (new v1+ SDK format)
client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

app = Flask(__name__)

@app.route("/")
def home():
    return "AI Code Reviewer is Live!"

@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.json
    print("Webhook received!")

    commits = data.get("commits", [])
    for commit in commits:
        print(f"Commit by: {commit['author']['name']}")
        print(f"Message: {commit['message']}")
        print("Files changed:")
        for file in commit.get("modified", []):
            print(f"- {file}")

        prompt = f"""You are a senior developer. Here's a commit message:
---
{commit['message']}
---
Please review the commit message and suggest improvements or issues."""

        try:
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a helpful and strict code reviewer."},
                    {"role": "user", "content": prompt}
                ]
            )
            reply = response.choices[0].message.content
            print("\n🔍 GPT Review:\n", reply)
        except Exception as e:
            print("⚠️ Error from OpenAI:", e)

    return {"status": "reviewed"}, 200

if __name__ == "__main__":
    app.run(port=5000)
"# comment added" 
"# comment added" 
