#!twitch-project/bin/python

import sqlite3
import argparse
import time
import numpy as np
from twitchstream.chat import TwitchChatStream
from json import dumps
from flask import Flask, url_for, g, render_template
from sqlalchemy import create_engine #modified
from flask.ext.jsonpify import jsonify

db_connect = create_engine('sqlite:///mydatabase.db')

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
    conn = db_connect.connect()
    query = conn.execute("select * from questions")
    question_list = {'id': [i[0] for i in query.cursor.fetchall()]}
    return jsonify(question_list)

@app.route('/questions/<number>', methods=['GET'])
def get_thequestions(number):
    conn = db_connect.connect()
    query = conn.execute("select * from questions where id = %d" %int(number))
    result = {'id': [dict(zip(tuple (query.keys()) ,i)) for i in query.cursor]}
    return jsonify(result)

@app.route('/voting/<number>', methods=['GET'])
def voting(number):

    conn = db_connect.connect()
    query = conn.execute("select * from questions where id = %d" %int(number))
    for row in query:
      DisplayQuestion = row[0];
      OptionOne = row[1];
      OptionTwo = row[2];
    scoreA = 0;
    scoreB = 0;
    with TwitchChatStream(username='wwyrd',oauth='oauth:v1exdo5jw9hmqrbozduymby6opyn6w',verbose=False) as chatstream:
	chatstream.send_chat_message('Voting is open!')
	timer = 60
	while timer > 0:
	    time.sleep(1)
            received = chatstream.twitch_receive_messages()
            if received:
                for chat_message in received:
                    print("Got a message '%s' from %s" % (
                        chat_message['message'],
                        chat_message['username']))
		    if chat_message['message'].lower() == 'a': scoreA += 1;
		    if chat_message['message'].lower() == 'b': scoreB += 1; 
	    timer-=1;
            print(timer)   
    result = {"OptionA":scoreA, "OptionB":scoreB}
    return jsonify(result)

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

if __name__ == '__main__':
    app.run(host='192.168.0.23')
