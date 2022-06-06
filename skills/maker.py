import markovify
import os
import random
import datetime

class maker():
    def __init__(self, config, events):
        events.add_command('maker', self.maker)

        # Open corpus
        rpath = os.path.dirname(os.path.realpath(__file__))
        with open(f'{rpath}/maker_corpus.txt', 'r') as f:
            corpus = f.read()

        # Create markov model
        random.seed(datetime.datetime.now())
        self.model = markovify.NewlineText(corpus, state_size=2)
        self.model.compile(inplace = True)

    def maker(self, data):
        random.seed(datetime.datetime.now())
        return self.model.make_short_sentence(120)
