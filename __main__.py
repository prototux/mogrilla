from mogrilla import Mogrilla
import signal
import argparse

# Parse arguments
argsp = argparse.ArgumentParser(prog='Mogrilla', description='Private messaging bot')
argsp.add_argument('--config', action='store', default='config.yml', help='Configuration file')
argsp.add_argument('--debug', action='store_true', help='Debug mode')
args = argsp.parse_args()

daemon = Mogrilla(config=args.config, debug=args.debug)
signal.signal(signal.SIGHUP, daemon.reload)
signal.signal(signal.SIGINT, daemon.exit)
signal.signal(signal.SIGTERM, daemon.exit)
daemon.start()
