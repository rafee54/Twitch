from twitchstream.chat import TwitchChatStream

chatstream = TwitchChatStream(username='kermitlefroge',oauth='oauth:7q0ihza8o2ftdm6xl8e20yl3kxtdgs',verbose=True)
chatstream.send_chat_message('fuckl')
while True:
            received = chatstream.twitch_receive_messages()
            if received:
                for chat_message in received:
                    print("Got a message '%s' from %s" % (
                        chat_message['message'],
                        chat_message['username']
                    ))
