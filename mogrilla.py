import sys
import logging
import yaml

from messaging import Messaging
from skills import Skills
from events import Events

class Mogrilla():
    def __init__(self, config='config.yml', debug=False):
        # Init logging
        self.debug = debug
        self.initLogging()

        # Load config
        self.config = {}
        self.logger.info('(core) loading configuration')
        self.loadConfig(config)
        if not self.config:
            self.logger.critical('(core) FATAL: invalid config!')
            sys.exit(1)
        else:
            self.logger.debug('(core) configuration loaded')

        # Init events handler
        self.events = Events(self.config.get('prefix', '!'))

        # Init skills
        self.loadSkills()

        # Init messaging thread
        self.loadMessaging()

        self.logger.info('(core) init done')

    def initLogging(self):
        # Create logger with debug level
        self.logger = logging.getLogger('mogrilla')
        self.logger.setLevel(logging.DEBUG)

        # Create the handler and configure it
        handler = logging.StreamHandler()
        handler.setLevel(logging.DEBUG if self.debug else logging.INFO)
        handler.setFormatter(logging.Formatter('%(levelname)s: %(message)s'))
        self.logger.addHandler(handler)

    def loadConfig(self, config_path):
        # If we reload, don't reset self.config
        new_config = {}

        with open(config_path, 'r') as config_file:
            try:
                new_config = yaml.load(config_file, Loader=yaml.SafeLoader)
            except yaml.YAMLError:
                self.logger.error('(core) error: invalid configuration file')
                return

        if not 'skills' in new_config:
            self.logger.error('(core) error: no skills in config')
            return

        if not 'messaging' in new_config:
            self.logger.error('(core) error: no messaging connector in config')
            return

        self.config = new_config


    def loadSkills(self):
        self.skills = Skills(self.config['skills'], self.events)

    def loadMessaging(self):
        self.messaging = Messaging(self.config['messaging'], self.events)

    def start(self):
        import time
        while True:
            time.sleep(10)

    def reload(self, signum, frame):
        self.logger.info('(core) reloading config')
        self.loadConfig()

    def exit(self, signum, frame):
        self.logger.info('(core) bye')
        sys.exit(0)
