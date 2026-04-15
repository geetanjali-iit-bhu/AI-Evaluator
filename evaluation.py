import json
import re
from groq import Groq
from vector_store import load_vector_store, retrieve_chunks

client = Groq()

EVAL_MODEL = "llama-3.3-70b-versatile"


def build_evaluation_prompt(question, context, student_answer, max_marks):
    return f"""
You are an IIT professor evaluating a student's answer.

You must:
1. Evaluate correctness
2. Give partial marks (VERY IMPORTANT)
3. Detect hallucinated or irrelevant content
4. Be strict but fair

------------------------
QUESTION:
{question}

------------------------
COURSE CONTEXT (RAG):
{context}

------------------------
STUDENT ANSWER:
{student_answer}

------------------------

MARKING RULES:
- Award partial marks for partially correct reasoning
- Deduct marks for incorrect or hallucinated statements
- Prefer step-by-step evaluation
- Final score must be between 0 and {max_marks}

Return STRICT JSON ONLY:
{{
  "score": <number>,
  "max_score": {max_marks},
  "breakdown": [
    {{"criterion": "...", "marks_awarded": ..., "reason": "..."}}
  ],
  "feedback": "..."
}}
"""


def evaluate_answer(question, student_answer, topic, max_marks=5, k=4):
    store = load_vector_store()

    chunks = retrieve_chunks(store, topic, k=k)

    context = "\n\n".join(
        [c.page_content for c in chunks]
    )

    prompt = build_evaluation_prompt(
        question, context, student_answer, max_marks
    )

    response = client.chat.completions.create(
    model=EVAL_MODEL,
    messages=[
        {
            "role": "system",
            "content": (
                "You are an automated exam evaluation engine.\n"
                "You MUST follow these rules STRICTLY:\n"
                "1. Output ONLY valid JSON.\n"
                "2. Do NOT include any explanation.\n"
                "3. Do NOT use markdown (no ```).\n"
                "4. Do NOT include text before or after JSON.\n"
                "5. Your response must start with '{' and end with '}'.\n"
                "6. Ensure JSON is syntactically valid.\n"
            )
        },
        {
            "role": "user",
            "content": prompt
        }
    ],
    temperature=0.2
)

    raw_output = response.choices[0].message.content

# ----------------------------
# STEP 1: Try direct JSON parse
# ----------------------------
    try:
        return json.loads(raw_output)
    except:
        pass

# ----------------------------
# STEP 2: Extract JSON from messy output
# ----------------------------
    try:
        match = re.search(r"\{.*\}", raw_output, re.DOTALL)
        if match:
            return json.loads(match.group())
    except:
        pass

# ----------------------------
# STEP 3: SAFE fallback (never crash)
# ----------------------------
    return {
        "error": "Invalid JSON from model",
        "raw_output": raw_output,
        "score": 0,
        "feedback": "Could not parse model response"
    }