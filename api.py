from dotenv import load_dotenv
load_dotenv()

from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
from rag_pipeline import generate_question_paper, ALL_RUBRIC_CRITERIA
import re, json

app = Flask(__name__)
CORS(app)

@app.route('/')
def index():
    return send_file('examforge.html')   # ← THIS WAS MISSING

@app.route('/generate', methods=['POST'])
def generate():
    body = request.get_json()
    topic      = body.get('topic', 'Data Structures and Algorithms')
    difficulty = body.get('difficulty', 'medium')
    num_mcq    = int(body.get('num_mcq', 5))
    num_short  = int(body.get('num_short', 3))
    num_long   = int(body.get('num_long', 2))
    rubric     = body.get('rubric', ['Conceptual clarity','Application ability'])

    raw = generate_question_paper(
        topic=topic, difficulty=difficulty,
        num_mcq=num_mcq, num_short=num_short, num_long=num_long,
        rubric_criteria=rubric
    )
    print("=== RAW LLM OUTPUT ===")
    print(raw)                        # ← ADD THIS
    print("======================")
    return jsonify({ "raw": raw, "topic": topic })

@app.route('/health')
def health():
    return jsonify({"status": "ok"})

from evaluation import evaluate_answer

@app.route('/evaluate-page')
def evaluate_page():
    return send_file('evaluate.html')

@app.route('/evaluate', methods=['POST'])
def evaluate():
    data = request.get_json()

    question = data.get("question")
    student_answer = data.get("answer")
    topic = data.get("topic", "Data Structures and Algorithms")
    max_marks = data.get("max_marks", 5)

    if not question or not student_answer:
        return jsonify({"error": "question and answer required"}), 400

    result = evaluate_answer(
        question=question,
        student_answer=student_answer,
        topic=topic,
        max_marks=max_marks
    )

    # SAFE JSON parsing
    try:
        if isinstance(result, dict):
            return jsonify(result)

        cleaned = result.strip()

        # remove markdown fences if any
        cleaned = cleaned.replace("```json", "").replace("```", "")

        return jsonify(json.loads(cleaned))

    except Exception as e:
        return jsonify({
            "error": "Model returned invalid JSON",
            "raw": result,
            "debug": str(e)
        }), 500

if __name__ == '__main__':
    app.run(port=8000, debug=True)