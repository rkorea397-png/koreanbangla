import json
import os
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)
ROOT = os.path.dirname(os.path.abspath(__file__))

def load_json(filename):
    with open(os.path.join(ROOT, "data", filename), encoding="utf-8") as f:
        return json.load(f)

LESSONS = load_json("lessons.json")
VOCAB = load_json("vocabulary.json")
QUIZ = load_json("quiz.json")

@app.route("/")
def home():
    q = request.args.get("q", "").strip().lower()
    lessons = LESSONS
    if q:
        lessons = [x for x in LESSONS if q in x["title"].lower() or q in x["intro"].lower()
                   or any(q in s["heading"].lower() or q in s["body"].lower() for s in x["sections"])]
    return render_template("index.html", lessons=lessons, total_lessons=len(LESSONS),
                           total_vocab=len(VOCAB), query=q)

@app.route("/lesson/<int:lesson_id>")
def lesson(lesson_id):
    item = next((x for x in LESSONS if x["id"] == lesson_id), None)
    if item is None:
        return render_template("not_found.html"), 404
    return render_template("lesson.html", lesson=item, total_lessons=len(LESSONS))

@app.route("/dictionary")
def dictionary():
    q = request.args.get("q", "").strip().lower()
    category = request.args.get("category", "").strip()
    results = [v for v in VOCAB if (not q or q in v["ko"].lower() or q in v["bn"].lower() or q in v["pron"].lower())
               and (not category or v.get("category") == category)]
    categories = sorted({v.get("category", "অন্যান্য") for v in VOCAB})
    return render_template("dictionary.html", words=results, categories=categories,
                           query=q, selected_category=category, total_vocab=len(VOCAB))

@app.route("/quiz")
def quiz_page():
    return render_template("quiz.html", quiz_count=len(QUIZ))

@app.route("/api/quiz")
def api_quiz():
    # Do not send answers to the browser before submission.
    safe = [{"id": i, "q": q["q"], "opts": q["opts"]} for i, q in enumerate(QUIZ)]
    return jsonify(safe)

@app.route("/api/quiz/submit", methods=["POST"])
def submit_quiz():
    data = request.get_json(silent=True) or {}
    answers = data.get("answers", {})
    correct = 0
    details = []
    for i, q in enumerate(QUIZ):
        submitted = answers.get(str(i))
        is_correct = submitted == q["answer"]
        if is_correct:
            correct += 1
        details.append({"id": i, "correct": is_correct, "answer": q["answer"],
                        "explain": q["explain"], "question": q["q"]})
    return jsonify({"score": correct, "total": len(QUIZ), "details": details})

@app.route("/api/vocabulary")
def api_vocabulary():
    q = request.args.get("q", "").strip().lower()
    result = [v for v in VOCAB if not q or q in v["ko"].lower() or q in v["bn"].lower() or q in v["pron"].lower()]
    return jsonify(result)

@app.route("/api/lessons")
def api_lessons():
    return jsonify(LESSONS)

if __name__ == "__main__":
    # Local development only. For production, use a WSGI server such as Gunicorn.
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)), debug=True)
