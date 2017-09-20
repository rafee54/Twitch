from __future__ import print_function
from twitchstream.outputvideo import TwitchOutputStreamRepeater
from twitchstream.chat import TwitchChatStream
import sqlite3
import random
import twitch
import time
import socket
import argparse
import numpy as np

parser = argparse.ArgumentParser(description=__doc__)
required = parser.add_argument_group('required arguments')
required.add_argument('-u', '--username',
                          help='twitch username',
                          required=True)
required.add_argument('-o', '--oauth',
                          help='twitch oauth '
                               '(visit https://twitchapps.com/tmi/ '
                               'to create one for your account)',
                          required=True)
args = parser.parse_args()

conn = sqlite3.connect('/home/pi/ServerProgram/mydatabase.db');

print("Opened the database sucessfully");

#VVV The portion of the project that keeps the number of records up to date

cursor = conn.execute("SELECT COUNT(a) FROM questions");
NoOfRecords = (cursor.fetchone()); #Returns the number of records.
number = (NoOfRecords[0]); #Number is the number of records as an int.
randomRecord = str((random.randint(1, number)));
#print(randomRecord);

#VVV Finds the random record and returns it

cursor = conn.execute("SELECT question, a, b FROM questions WHERE id = ?", (randomRecord))
for row in cursor: 
  DisplayQuestion = row[0];
  OptionOne = row[1];
  OptionTwo = row[2];
print(DisplayQuestion, OptionOne, OptionTwo);
chatmessage = ("Voting has opened. Type A to vote for %s. Type B to vote for %s." % (OptionOne, OptionTwo))
with TwitchChatStream(username=args.username,
	                  oauth=args.oauth,
	                  verbose=False) as chatstream:
	chatstream.send_chat_message(chatmessage)

scoreA = 0;
scoreB = 0;

timer = 10;
while timer > 0:
  time.sleep(1)
  received = chatstream.twitch_receive_messages();
  if received:
    d=received[0];
    #print(d["message"]);
    if d["message"] == "a" or d["message"] == "A":
      scoreA+=1;
    if d["message"] == "b" or d["message"] == "B":
      scoreB+=1;
  timer-=1;
  print(timer)

print("Score A: ", scoreA);
print("Score B: ", scoreB);

if scoreA == scoreB:
  print("equal scores")
elif scoreA > scoreB:
  print("Option A wins")
elif scoreA < scoreB:
  print("Option B wins")

cursor = conn.execute("UPDATE questions SET aResult=?, bResult=? WHERE id=?",(str(scoreA),str(scoreB), randomRecord))
conn.commit()


print ("Operation is complete");
conn.close;
