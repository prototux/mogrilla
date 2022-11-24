import logging
import importlib
import os

class Skills():
    def __init__(self, global_config, events):
        self.skills = {}
        self.logger = logging.getLogger('mogrilla')
        self.logger.info('Loading skills plugins')

        rpath = os.path.dirname(os.path.realpath(__file__))
        for name, config in global_config.items():
            try:
                spec = importlib.util.spec_from_file_location(name, f'{rpath}/skills/{name}/skill.py')
                module = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(module)
                self.skills[name] = getattr(module, name)(config, events)
                self.logger.info(f'Loaded skill plugin {name}')
            except (ImportError, AttributeError) as e:
                self.logger.error(f'Cannot load skill plugin {name}: {e}')
