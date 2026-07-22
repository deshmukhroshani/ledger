from google import genai
from google.genai import types
from flask import Flask, request, jsonify
import os

#genai.configure()  # Uses Application Default Credentials (no API key)

#model = genai.GenerativeModel("gemini-1.5-flash-latest")
client = genai.Client(
            vertexai=True,
            project="hack-team-off-the-ledger",
            location="europe-west1")
            

app = Flask(__name__)

@app.route("/generate", methods=["GET"])
def generate():
    prompt = request.args.get("prompt", "Hello from Gemini!")
    try:
        #response = model.generate_content(prompt)
        response = client.models.generate_content(model='gemini-2.0-flash-001',contents='Why is the sky blue?')
        print(response.text)
        return jsonify({"response": response.text})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/", methods=["GET"])
def root():
    return (
        "Use /generate?prompt=your_text to get Gemini Flash response, "
        "e.g., /generate?prompt=Tell+me+a+joke"
    )

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)
