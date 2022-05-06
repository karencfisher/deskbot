import os

from basic_bot import Bot
from eliza import Eliza

class ElizaBot(Bot):
    def __init__(self):
        super().__init__()
        self.eliza = Eliza()
        self.eliza.load('doctor.txt')

    def listening(self, listening_flag):  
        print("Begin process:", os.getpid())
        greeting = self.eliza.initial()
        self.talk.talk(greeting)
        while listening_flag.value:  
            text = self.listen.listen()
            if text == '':
                continue
            response = self.eliza.respond(text)
            if response is None:  
                listening_flag.value = False
            else:
                self.talk.talk(response)
        print('Exiting process:', os.getpid())


def main():
    bot = ElizaBot()
    bot.run()

if __name__ == '__main__':
    main()