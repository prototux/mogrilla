import requests
import logging
import json

class ddodg():
    def __init__(self, config, events):
        self.logger = logging.getLogger('mogrilla')
        self.events = events
        events.add_command('ddodg', self.ddodg)


    def ddodg(self, data):
        msg = data['message']
        author = data['author']
        self.logger.info(f'Got politics for {msg}')

        headers = {
            'authority': 'chatswrap.com',
            'origin': 'https://degaucheoudedroite.delemazure.fr',
            'referer': 'https://degaucheoudedroite.delemazure.fr/',
            'user-agent': 'Mozilla/5.0 (X11; Linux x86_64)',
            'accept': '*/*',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'cross-site'
        }

        data = {
            'input': msg,
            'price': 2
        }

        res = requests.post(
            url = 'https://degaucheoudedroite.delemazure.fr/api.php',
            headers = headers,
            data = json.dumps(data)
        )
        ret = res.json()

        if ret:
            return f'{author.mention}, {msg} est{ret["data"].lower()}'
        else:
            return 'Si a 3j d\'uptime tu as pas un 503 tu as un peu raté ta vie'
