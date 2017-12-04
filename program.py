#!twitch-project/bin/python

## from __future__ import print_function        This is for python 2 compatibility, not needed due to virtual environment.
from twitchstream.outputvideo import TwitchOutputStreamRepeater
from twitchstream.chat import TwitchChatStream
import sqlite3
import random
import twitch     #                             Is this necessary?
import time #                             Only import what is necessary, loading full libraries is bad practice
# import socket                                 Unnecessary import as it is not used
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

conn = sqlite3.connect('./mydatabase.db'); # Relative file name so does not depend on directory name

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
	                  verbose=True) as chatstream:
	chatstream.send_chat_message(chatmessage)

scoreA = 0;
scoreB = 0;

timer = 10;
while timer > 0:
  time.sleep(1)
  received = chatstream.twitch_receive_messages();
  if received:
   for chat_message in received:
    	d=received[0];
    	print(d["message"]);
    	if d["message"] == "a" or d["message"] == "A":
      		scoreA+=1;
    	if d["message"] == "b" or d["message"] == "B":
      		scoreB+=1;
  timer-=1;
  print(timer)

print("Score A: ", scoreA);
print("Score B: ", scoreB);

if scoreA == scoreB:
  chatstream.send_chat_message("Equal scores") 
  print("equal scores")
elif scoreA > scoreB:
  print("Option A wins")
  chatstream.send_chat_message("Option A wins")
elif scoreA < scoreB:
  print("Option B wins")
  chatstream.send_chat_message("Option B wins")

cursor = conn.execute("UPDATE questions SET aResult=?, bResult=? WHERE id=?",(str(scoreA),str(scoreB), randomRecord))
conn.commit()


print ("Operation is complete");
conn.close;
