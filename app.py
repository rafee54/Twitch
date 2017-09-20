#!twitch-project/bin/python
from flask import Flask, url_for

def make_public_question(question):
    new_question = {}
    for field in question:
        if field == 'id':
            new_question['uri'] = url_for('get_question',question_id=question['id'], _external=True)
        else:
            new_question[field] = question[field]
    return new_question

app = Flask(__name__)

@app.route('/questions', methods=['GET'])
def get_questions():
    return "This is the questions page"

if __name__ == '__main__':
    app.run(debug=True)
