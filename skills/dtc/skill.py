from crawlerpy.dtc import DtcCrawler
import random

class dtc():
    def __init__(self, config, events):
        self.events = events
        self.dtc = DtcCrawler()
        events.add_command('dtc', self.quote)

    def getquote(self):
        ret, resp = self.dtc.random()
        art = random.choice(resp)
        text = ''
        for section in art.sections:
            for data in section.contents:
                quote = data.value.split(':', 1)
                if not len(quote) == 2:
                    return None
                text+= f'**{quote[0]}**: {quote[1]}\n'
        return text


    def quote(self, data):
        qte = None
        tries = 0
        while qte == None and tries < 10:
            qte = self.getquote()
            tries += 1

        return qte
