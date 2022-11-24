import logging

class hello():
    def __init__(self, config, events):
        events.add_command('hello', self.hello)
        self.logger = logging.getLogger('mogrilla')


    def hello(self, data):
        author = data['author']
        self.logger.info(f'Got hello from {author}')
        return f'Hello {author.mention}!'
