import markovify
import os
import random
import time

class maker():
    def __init__(self, config, events):
        events.add_command('maker', self.maker)

        # Open corpus
        rpath = os.path.dirname(os.path.realpath(__file__))
        with open(f'{rpath}/corpus.txt', 'r') as f:
            corpus = f.read()

        # Create markov model
        random.seed(time.time())
        self.model = markovify.NewlineText(corpus, state_size=2)
        self.model.compile(inplace = True)

    def maker(self, data):
        random.seed(time.time())
        return self.model.make_short_sentence(120)
