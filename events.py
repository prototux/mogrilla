import logging

class Events():
    def __init__(self):
        self.commands = {}
        self.logger = logging.getLogger('mogrilla')

    def add_command(self, name, handler):
        self.commands[name] = handler

    def handle_command(self, command, data):
        self.logger.info(f'got command {command}')
        if not command in self.commands:
            self.logger.error('Error: no command')
            return

        return self.commands[command](data)

    def handle_message(self, message, author):
        if message.startswith('!'):
            if len(message.split(' ',1)) == 1:
                command = message.replace('!', '')
                message = ''
            else:
                command = message.split(' ',1)[0].replace('!', '')
                message = message.split(' ',1)[1]

            return self.handle_command(command, {'message': message, 'author': author})
