from flask import Flask, request, render_template, redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from surveys import satisfaction_survey as survey

RESPONSE = "responses"

app = Flask(__name__)
app.config['SECRET_KEY'] = "secret"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

debug = DebugToolbarExtension(app)

@app.route('/')
def home():
    
    return render_template('home.html', survey=survey)

@app.route('/begin', method=["POST"])
def start_survey():
    
    session[RESPONSE] = []
    
    return redirect('/questions/0')

@app.route('/answer', method=['POST'])
def add_answer():
    choice = request.form['answer']
    responses = session[RESPONSE]
    responses.append(choice)
    session[RESPONSE] = responses

    if (len(responses) == len(survey.questions)):
        return redirect('/thank_you.html')
    
    else:
        return redirect(f'/questions/{len(responses)}')

@app.route('/questions/<int:qid>')
def  show_question(qid):

    responses = session.get(RESPONSE)

    if (responses is None):
        return redirect('/')
    
    if (len(responses) == len(survey.questions)):
        return redirect('/thank_you')
    
    if (len(responses) != qid):
        flash(f'Invaild Question Id: {qid}')
        return redirect(f'/questions/{len(responses)}')

@app.route('/thenak_you')
def thank_you():
    return render_template('thank _you.html')
