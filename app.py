from flask import Flask, request, jsonify, render_template
from hf import generate_response

app = Flask(__name__)

SYSTEM_PROMPT = """
You are a professional AI teaching assistant.
Explain clearly with headings, bullet points, and examples.
"""

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    data = request.json
    user_message = data.get("message", "")

    prompt = f"{SYSTEM_PROMPT}\nUser:{user_message}\nAssistant:"
    response = generate_response(prompt, temperature=0.5, max_tokens=700)

    return jsonify({"reply" : response})

if __name__ == "__main__":
    app.run(debug=True)