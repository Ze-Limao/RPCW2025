# Backend & Frontend: app.py (Flask with Jinja templates)
from flask import Flask, render_template, request, session, redirect, url_for
from flask_cors import CORS
import ssl
import certifi
from fetch_questions import fetch_questions_from_dbpedia

ssl._create_default_https_context = ssl._create_unverified_context

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'
CORS(app)

@app.route('/')
def home():
    session['score'] = 0
    session['questions'] = fetch_questions_from_dbpedia()
    return redirect(url_for('quiz'))

@app.route('/quiz', methods=['GET', 'POST'])
def quiz():
    questions = session.get('questions', [])
    if request.method == 'POST':
        user_answer = request.form.get('answer')
        question_text = request.form.get('question')

        for question in questions:
            if question['question'] == question_text:
                correct = question['answer'] == user_answer
                session['score'] = session.get('score', 0) + (1 if correct else 0)
                session['questions'] = questions[:-1]
                return render_template('result.html', correct=correct, correct_answer=question['answer'], score=session['score'])
        print("Question not found in session!")

    if questions:
        question = questions[-1]
        return render_template('quiz.html', question=question)
    else:
        return redirect(url_for('score'))

@app.route('/score')
def score():
    return render_template('score.html', score=session.get('score', 0))

if __name__ == '__main__':
    app.run(debug=True)
