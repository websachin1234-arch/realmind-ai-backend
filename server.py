from flask import Flask, request, jsonify
from flask_cors import CORS
from groq import Groq
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)
CORS(app)

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

PORT = int(os.getenv("PORT", 3000))


@app.route("/api/chat", methods=["POST"])
def chat():
    try:
        data = request.get_json()
        message = data.get("message", "")

        completion = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {
                    "role": "user",
                    "content": message
                }
            ]
        )

        reply = completion.choices[0].message.content

        return jsonify({
            "reply": reply
        })

    except Exception as e:
        print(e)
        return jsonify({"error": str(e)}), 500


@app.route("/api/proposal", methods=["POST"])
def proposal():
    try:
        data = request.get_json()

        prompt = f"""
Generate a professional website proposal.

Client Name: {data.get('fullName')}
Business: {data.get('business')}
Website Type: {data.get('websiteType')}
Budget: {data.get('budget')}
Timeline: {data.get('timeline')}
Pages: {data.get('pages')}
Company Size: {data.get('companySize')}
Description: {data.get('description')}

Include:
1. Project Complexity
2. Features
3. Tech Stack
4. Timeline
5. SEO
6. Summary
"""

        completion = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        )

        recommendation = completion.choices[0].message.content

        return jsonify({
            "recommendation": recommendation
        })

    except Exception as e:
        print(e)
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    print(f"Server Running on Port {PORT}")
    app.run(host="0.0.0.0", port=PORT, debug=True)