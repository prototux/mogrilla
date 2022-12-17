import requests
import discord as dislib
import logging
import threading
import asyncio
import time

class discord():
    # Discord client
    class Client(dislib.Client):
        def __init__(self, logger, events, intents):
            self.logger = logger
            self.events = events
            intents = dislib.Intents.default()
            intents.message_content = True
            super().__init__(intents=intents)

        async def on_ready(self):
            self.logger.info(f'(discord) logged on as {self.user}')

        async def on_message(self, message):
            # Ignore self messages
            if message.author == self.user:
                return

            self.logger.info(f'(discord) message from {message.author}: {message.content}')

            ret = self.events.handle_message(message.content, message.author)
            self.logger.info(ret)
            if ret:
                self.logger.info(f'(discord) ==> {ret}')
                await message.channel.send(ret)

    def __init__(self, config, events):
        self.logger = logging.getLogger('mogrilla')
        self.logger.info('(discord) Init plugin')

        if not 'token' in config:
            self.logger.error('(discord) error: no token in config')
            return

        self.events = events
        self.config = config

        self.messages = []

        threading.Thread(target=self.run, daemon=True).start()
        threading.Thread(target=self.messenger, daemon=True).start()

    def add_msg(self, chan, message, file=None):
        self.logger.info(f'(discord) got message for chan {chan}')
        self.messages.append({'chan': chan, 'msg': message, 'file': file})

    def messenger(self):
        while True:
            if len(self.messages) > 0:
                message = self.messages.pop()
                self.logger.info(f'(discord) sending message for chan {message["chan"]}')
                self.loop.create_task(self.send_msg(message['chan'], message['msg'], message['file']))
            time.sleep(0.01)

    def run(self):
        self.loop = asyncio.new_event_loop()
        asyncio.set_event_loop(self.loop)

        intents = dislib.Intents.default()
        #intents.message_content = True

        self.client = self.Client(self.logger, self.events, intents=intents)

        self.loop.create_task(self.client.start(self.config['token']))
        self.loop.run_forever()

    async def send_msg(self, chan, message, file=None):
        self.logger.info(f'(discord) sending {message} to {chan}')

        for channel in self.client.get_all_channels():
            if channel.name == chan:
                self.logger.info('(discord) => found chan')
                await channel.send(message, file=file)
