import json
import re

def parse_question_paper(raw: str):
    """
    Converts LLM paper → structured evaluation-ready format
    """

    questions = []
    current = None
    mode = None

    lines = raw.split("\n")

    for line in lines:
        line = line.strip()

        # Detect question
        q = re.match(r"Q(\d+)\.\s*(.*)", line)
        if q:
            if current:
                questions.append(current)

            current = {
                "id": f"Q{q.group(1)}",
                "text": q.group(2),
                "type": "unknown",
                "options": {},
                "answer": None,
                "rubric": [],
                "marks": 0
            }
            continue

        # MCQ options
        if current and "(a)" in line and "(b)" in line:
            opts = re.findall(r"\(([a-d])\)\s*([^()]+)", line)
            current["options"] = {k: v.strip() for k, v in opts}
            current["type"] = "mcq"

        # Answer
        if current and line.lower().startswith("answer"):
            m = re.findall(r"[a-d]", line.lower())
            if m:
                current["answer"] = m[0]

        # Marking scheme
        if current and ":" in line:
            if "marking" not in line.lower():
                parts = line.split(":")
                if len(parts) == 2:
                    try:
                        current["rubric"].append({
                            "criterion": parts[0].strip("-• "),
                            "marks": int(parts[1].strip())
                        })
                        current["marks"] += int(parts[1].strip())
                    except:
                        pass

    if current:
        questions.append(current)

    return questions