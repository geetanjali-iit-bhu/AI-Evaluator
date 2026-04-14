# api.py
from dotenv import load_dotenv
load_dotenv()

from flask import Flask, request, jsonify
from flask_cors import CORS
from rag_pipeline import generate_question_paper, ALL_RUBRIC_CRITERIA
import re, json

app = Flask(__name__)
CORS(app)  # allows the HTML file to call this API

@app.route('/generate', methods=['POST'])
def generate():
    body = request.get_json()
    topic     = body.get('topic', 'Data Structures and Algorithms')
    difficulty= body.get('difficulty', 'medium')
    num_mcq   = int(body.get('num_mcq', 5))
    num_short = int(body.get('num_short', 3))
    num_long  = int(body.get('num_long', 2))
    rubric    = body.get('rubric', ['Conceptual clarity','Application ability'])

    raw = generate_question_paper(
        topic=topic, difficulty=difficulty,
        num_mcq=num_mcq, num_short=num_short, num_long=num_long,
        rubric_criteria=rubric
    )

    return jsonify({ "raw": raw, "topic": topic })

@app.route('/health')
def health():
    return jsonify({"status": "ok"})

if __name__ == '__main__':
    app.run(port=8000, debug=True)