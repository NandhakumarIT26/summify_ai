from flask import Flask, render_template, request, jsonify
import os
import requests
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

@app.route('/', methods=['GET', 'POST'])

def index():
    summary = None
    if request.method == 'POST':
        word_count = request.form['words']
        input_text = request.form['userText']
        summary = summarize_text(input_text,word_count)
    return render_template('index.html', summary=summary)

def summarize_text(text,words):
    url = "https://api.groq.com/openai/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": "llama3-8b-8192",
        "messages": [
            {"role": "system", "content": "You are a helpful assistant that summarizes text."},
            {"role": "user", "content": f"Summarize the following text:\n{text} in to {words} words"}
        ],
        "temperature": 0.5
    }

    response = requests.post(url, headers=headers, json=payload)

    # 🔍 Add debug print

    if response.status_code == 200:
        return response.json()['choices'][0]['message']['content']
    else:
        return "Sorry, the AI service failed to summarize your text."

if __name__ == '__main__':
    app.run(debug=True)
