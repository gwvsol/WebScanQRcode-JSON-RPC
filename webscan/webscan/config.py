from os import getenv as env
from pathlib import Path


class ConfigError(Exception):
    pass


# =====================================================
#
WEBSCAN_WEBCAM = env('WEBSCAN_WEBCAM', default=None)
if WEBSCAN_WEBCAM is None:
    raise ConfigError('WEBSCAN_WEBCAM ERROR in env')
WEBSCAN_DEV = Path(WEBSCAN_WEBCAM)
if not WEBSCAN_DEV.exists():
    raise ConfigError(f'{WEBSCAN_WEBCAM} => There is not in the system')
#
# =====================================================
#
WEBSCAN_DATA = dict()
WEBSCAN_DATA.update({'ping': 'OK', 'status': 'ScanOFF',
                     'scan': [], 'help': {}})
WEBSCAN_HELP = WEBSCAN_DATA.get('help')
WEBSCAN_HELP.update({
    'ping': 'Method for checking the service',
    'enable': 'Method for enabling the QR scanner',
    'disable': 'Method for turning off the QR scanner',
    'getscan': 'Method for reading data from a QR scanner',
    'help': 'Method for getting information about working with the service'})

WEBSCAN_BARCODES = set()
#
# =====================================================
#
