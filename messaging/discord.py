import requests
import discord as dislib
import logging
import threading
import asyncio

class discord():
    # Discord client
    class Client(dislib.Client):
        def __init__(self, logger, events, intents):
            self.logger = logger
            self.events = events
            super().__init__(intents=intents)

        async def on_ready(self):
            self.logger.info(f'Logged on as {self.user}')

        async def on_message(self, message):
            # Ignore self messages
            if message.author == self.user:
                return

            self.logger.info(f'Message from {message.author}: {message.content}')

            ret = self.events.handle_message(message.content, message.author)
            if ret:
                self.logger.info(f'==> {ret}')
                await message.channel.send(ret)

    def __init__(self, config, events):
        self.logger = logging.getLogger('mogrilla')
        self.logger.info('Init discord plugin')

        if not 'token' in config:
            self.logger.error('discord: no token in config')
            return

        intents = dislib.Intents.default()
        #intents.message_content = True

        self.client = self.Client(self.logger, events, intents=intents)

        loop = asyncio.get_event_loop()
        loop.create_task(self.client.start(config['token']))
        threading.Thread(target=loop.run_forever, daemon=True).start()
