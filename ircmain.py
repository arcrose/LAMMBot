import ircapi
from chatbot import *
import config as ircconfig
import random
import string

class ChatBot(object):
    def __init__(self):
        ircapi.connect(ircconfig.server[0], ircconfig.server[1], False)
        ircapi.setNick(ircconfig.bot_nick)
        self.words = load_hash()
        # Gives us access to everything from ircapi through instances of
        # this class, to make things a little more intuitive.
        for key in ircapi.__dict__: self.__dict__[key] = ircapi.__dict__[key]
    
    def _strip_punctuation(self, s):
        if not s: return ""
        if s[0] in string.punctuation:
            return self._strip_punctuation(s[1:])
        return s[0] + self._strip_punctuation(s[1:])

    def handle_event(self, event):
        if event is None: return
        if "PING" in event: ircapi.handle_ping(event)
        if "please choose a different nick" in event:
            ircapi.identify(ircconfig.password)
        if "(Ping timeout" in event: 
            ircapi.disconnect()
            return "FINISHED"
        if "PRIVMSG" in event:
            content = event.split("PRIVMSG")[1][1:]
            if not content.startswith("#"): continue
            msg = content.split()[1:]
            msg[0] = msg[0].replace(":", "")
            response = reply(self._strip_punctuation(" ".join(msg).lower()), self.words)
            if random.randint(0, 100) <= ircconfig.reply_chance and response is not None:
                print "Responding: " + response
                ircapi.sendMessage(content.split()[0], response)

    def start(self):
        event = ""
        while not "you are now recognized" in event:
            event = ircapi.readEvent()
            self.handle_event(event)
        for channel in ircconfig.channels:
            ircapi.sendJoin(channel)
        while True:
            try:
                event = ircapi.readEvent()
                print "-*- Event: " + event
                self.handle_event(event)
            except KeyboardInterrupt:
                ircapi.disconnect()
                return

if __name__ == "__main__":
    chatbot = ChatBot()
    chatbot.start()
