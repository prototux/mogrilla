import logging
import threading
import time
import re
import socket

class quake():
    def __init__(self, config, events):
        self.events = events
        self.logger = logging.getLogger('mogrilla')
        self.config = config

        self.player_regex = re.compile(r'^(\-?\d+) (\d+) "(.*)"')

        if not 'server' in self.config:
            self.logger.error('(quake) error: no server in config')
            return

        if not 'chan' in self.config:
            self.logger.error('(quake) error: no chan in config')
            return

        self.client = rcon(self.logger, self.config['server'], self.config.get('password'))
        self.thread = threading.Thread(target=self.run, daemon=True)
        self.thread.start()

        # Current game data
        self.map = ''
        self.players = []

    def run(self):
        self.client.connect()
        while True:
            # Reconnect if disconnected
            if not self.client.cmd('getinfo'):
                self.logger.error('(quake) error: got disconnected, reconnecting...')
                self.client.connect()

            # Get current data
            curmap = self.map
            curplayers = self.players

            # Update infos
            self.update()

            # If there's no data (eg. first loop iteration), ignore
            if not curmap:
                continue

            # Check if the map changed (eg. last match finished), and send stats
            if curmap != self.map:
                # Only send if there was players during the match
                if curplayers:
                    cnt = f'Stats for {curmap}:\n'
                    for player in curplayers:
                        cnt+=f'**{player["name"]}**: {player["frags"]}\n'
                    self.events.send_message(self.config['chan'], cnt)

            # Wait a second before updating
            time.sleep(2)

    def update(self):
        ret = self.client.cmd('getstatus')
        if not ret:
            self.logger.error('(quake) error: no status data')
            return

        data = ret['data']

        raw_vars, raw_players = data[1:].split(b'\n', 1)

        # Get vars
        split  = raw_vars.split(b'\\')
        sane = []
        for item in split:
            sane.append(item.decode('utf-8'))
        self.vars = dict(zip(sane[::2], sane[1::2]))
        self.map = self.vars.get('mapname')

        # Get players
        self.players = []
        for player in raw_players.split(b'\n'):
            # Ignore empty lines
            if not player:
                continue

            raw_player = self.player_regex.match(player.decode('utf-8'))
            if not raw_player:
                self.logger.warn(f'(quake) warn: cannnot match player {player}')
                continue

            frags, ping, name = raw_player.groups()
            self.players.append({'name': name, 'frags': frags, 'ping': ping})

class rcon():
    def __init__(self, logger, server, password):
        # Network setup
        self.packet_prefix = b'\xff\xff\xff\xff'
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.logger = logger

        # Setup server
        self.password = password
        try:
            self.address, self.port = server.split(':')
            self.port = int(self.port)
            self.logger.info(f'(quake) init client for server {self.address} and port {self.port}')
        except:
            self.logger.error('(quake) rcon error: eerver must be in "addr:port" format')

    def connect(self):
        if not self.address or not self.port:
            self.logger.error('(quake) rcon error: eannot connect without address and port')
            return

    def send(self, data):
        self.sock.sendto(b''.join([self.packet_prefix, str.encode(data), b'\n']), (self.address, self.port))

    def recv(self, timeout=5):
        self.sock.settimeout(timeout)
        try:
            return self.sock.recvfrom(4096)
        except(socket.error) as e:
            self.logger.error(f'(quake) rcon error: error receiving data: {e}')

    def cmd(self, cmd, timeout=5, retries=3):
        while retries:
            self.send(cmd)
            try:
                data = self.recv(timeout)
            except:
                data = None

            if data:
                return self.parse(data[0])

            retries -= 1
        self.logger.error('(quake) rcon error: command timed out')

    def rcon_cmd(seld, cmd):
        if not self.password:
            self.logger.error('(quake) rcon error: Cannot rcon without password')
            return

        ret = self.cmd(f'rcon "{self.rcon_password}" {cmd}')
        if r[1] == 'No rconpassword set on the server.\n' or r[1] == 'Bad rconpassword.\n':
            self.logger.error(f'(quake) rcon error: error during rcon command: {r[1]}')

    def parse(self, data):
        if data.find(self.packet_prefix) != 0:
            self.logger.error('(quake) rcon error: malformed packet (no prefix)')
            return

        fl_len = data.find(b'\n')
        if fl_len == -1:
            self.logger.error('(quake) rcon error: malformed packet (no newline)')

        ret = {
            'type': data[len(self.packet_prefix):fl_len],
            'data': data[fl_len+1:]
        }
        return ret
