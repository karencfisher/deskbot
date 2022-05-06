import os

from basic_bot import Bot
from eliza import Eliza

class ElizaBot(Bot):
    def __init__(self):
        super().__init__()
        self.__eliza = Eliza()
        self.__eliza.load('doctor.txt')

    def listening(self, listening_flag):  
        print("Begin process:", os.getpid())
        greeting = self.__eliza.initial()
        self.__talk.talk(greeting)
        while listening_flag:  
            text = self.__listen.listen()
            if text == '':
                continue
            response = self.__eliza.respond(text)
            if text is None:  
                listening_flag = False
            else:
                self.__talk.talk(text)
        print('Exiting process:', os.getpid())


def main():
    bot = ElizaBot()
    bot.run()