import logging
import asyncio

class Events():
    def __init__(self, prefix):
        self.commands = {}
        self.logger = logging.getLogger('mogrilla')
        self.messenger = None
        self.prefix = prefix

    def add_command(self, name, handler):
        self.commands[name] = handler

    def handle_command(self, command, data):
        self.logger.info(f'(events) got command {command}')
        if not command in self.commands:
            self.logger.error('(events) error: no command')
            return

        return self.commands[command](data)

    def handle_message(self, message, author):
        if message.startswith(self.prefix):
            if len(message.split(' ',1)) == 1:
                command = message.replace(self.prefix, '')
                message = ''
            else:
                command = message.split(' ',1)[0].replace(self.prefix, '')
                message = message.split(' ',1)[1]

            return self.handle_command(command, {'message': message, 'author': author})

    def send_message(self, chan, message, file=None):
        self.logger.info(f'(events) got message for chan {chan}')
        if self.messenger:
            self.messenger.add_msg(chan, message, file)
        else:
            self.logger.error('(events) error: no messenger')

    def hl(self, username):
        pass

    def connect_voice(self, chan):
        pass

    def disconnect_voice(self):
        pass

    def send_voice(self, stream):
        pass
