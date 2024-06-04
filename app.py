from flask import Flask, render_template, request, redirect, url_for, session
import json

app = Flask(__name__)
app.secret_key = 'supersecretkey'

def load_questions():
    with open('data/questions.json') as f:
        return json.load(f)

@app.route('/')
def index():
    session.clear()
    return render_template('index.html')

@app.route('/question/<int:question_id>', methods=['GET', 'POST'])
def question(question_id):
    questions = load_questions()
    if question_id >= len(questions):
        return redirect(url_for('result'))

    if request.method == 'POST':
        selected_answer = int(request.form.get('answer'))
        correct_answer = questions[question_id]['correct']

        if 'score' not in session:
            session['score'] = 0

        if selected_answer == correct_answer:
            session['score'] += 1
        
        else:
            session['score'] = 0

        return redirect(url_for('question', question_id=question_id + 1))

    question = questions[question_id]
    return render_template('question.html', question=question, question_id=question_id, total_questions=len(questions))

@app.route('/result')
def result():
    score = session.get('score', 0)
    questions = load_questions()
    total_questions = len(questions)
    return render_template('result.html', score=score, total_questions=total_questions)

if __name__ == '__main__':
    app.run(debug=True)
