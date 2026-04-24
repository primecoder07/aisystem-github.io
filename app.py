from flask import Flask, render_template, request, jsonify
import PyPDF2

app = Flask(__name__)

# -------- Resume Text Extraction --------
def extract_text(file):
    text = ""
    reader = PyPDF2.PdfReader(file)
    for page in reader.pages:
        content = page.extract_text()
        if content:
            text += content
    return text.lower()

# -------- Resume Skill Analysis --------
def analyze_resume(text):
    scores = {
        "Software Development": 0,
        "Data Science": 0,
        "Cyber Security": 0
    }

    if "python" in text:
        scores["Software Development"] += 2
        scores["Data Science"] += 2

    if "java" in text:
        scores["Software Development"] += 2

    if "machine learning" in text:
        scores["Data Science"] += 3

    if "network" in text or "security" in text:
        scores["Cyber Security"] += 3

    return scores

# -------- Routes --------
@app.route('/')
def home():
    return render_template("index.html")

@app.route('/analyze', methods=['POST'])
def analyze():
    file = request.files['resume']
    q1 = int(request.form['q1'])
    q2 = int(request.form['q2'])

    # Resume Processing
    text = extract_text(file)
    resume_scores = analyze_resume(text)

    # SWOT Scores
    swot_scores = {
        "Software Development": q1,
        "Data Science": q2,
        "Cyber Security": (q1 + q2) // 2
    }

    # Final Weighted Score
    final_scores = {}
    for field in resume_scores:
        final_scores[field] = (
            resume_scores[field] * 0.6 +
            swot_scores[field] * 0.4
        )

    # Best Career
    best_career = max(final_scores, key=final_scores.get)

    reason = f"Based on your resume and SWOT test, {best_career} is the most suitable career for you."

    return jsonify({
        "career": best_career,
        "reason": reason
    })

# -------- Run Server --------
if __name__ == '__main__':
    app.run(debug=True)
