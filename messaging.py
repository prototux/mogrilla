import logging
import importlib
import os
import sys

class Messaging():
    def __init__(self, global_config, events):
        self.messagers = {}
        self.logger = logging.getLogger('mogrilla')
        self.logger.info('(messaging) loading messaging plugins')

        rpath = os.path.dirname(os.path.realpath(__file__))

        if len(global_config.items()) > 1:
            self.logger.error('(messaging) error: only one messaging client can be used')
            sys.exit(1)

        for name, config in global_config.items():
            try:
                spec = importlib.util.spec_from_file_location(name, f'{rpath}/messengers/{name}.py')
                module = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(module)
                self.messagers[name] = getattr(module, name)(config if config else {}, events)
                events.messenger = self.messagers[name]
                self.logger.info(f'(messaging) loaded messaging plugin {name}')
            except (ImportError, AttributeError) as e:
                self.logger.error(f'(messaging) error: cannot load messaging plugin {name}: {e}')
