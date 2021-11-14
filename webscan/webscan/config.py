from os import getenv as env


class ConfigError(Exception):
    pass


# =====================================================
#
REGION = env('REGION', default=None)
if REGION is None:
    raise ConfigError('REGION ERROR in env')
#
TOKEN_PRIVATE_KEY = env('TOKEN_PRIVATE_KEY', default=None)
if TOKEN_PRIVATE_KEY is None:
    raise ConfigError('TOKEN_PRIVATE_KEY ERROR in env')
#
TOKEN_EXPIRE_MINUTE = env('TOKEN_EXPIRE_MINUTE', default=None)
if TOKEN_EXPIRE_MINUTE.isdigit():
    TOKEN_EXPIRE_MINUTE = int(TOKEN_EXPIRE_MINUTE)
else:
    raise ConfigError('TOKEN_EXPIRE_MINUTE ERROR in env')
#
ALGORITHM = "HS256"
#
# =====================================================
#
if env('POSTGRESQL_SERVICE', default='Off') in \
        ['on', 'On', 'ON', '1', 'True', 'TRUE', 'true']:
    POSTGRESQL_SERVICE = True
else:
    POSTGRESQL_SERVICE = False
#
POSTGRESQL_HOST = env('POSTGRESQL_HOST', default=None)
if POSTGRESQL_HOST is None:
    raise ConfigError('POSTGRESQL_HOST ERROR in env')
#
POSTGRESQL_PORT = env('POSTGRESQL_PORT', default=None)
if POSTGRESQL_PORT.isdigit():
    POSTGRESQL_PORT = int(POSTGRESQL_PORT)
else:
    raise ConfigError('POSTGRESQL_PORT ERROR in env')
#
POSTGRESQL_USER = env('POSTGRESQL_USER', default=None)
if POSTGRESQL_USER is None:
    raise ConfigError('POSTGRESQL_USER ERROR in env')
#
POSTGRESQL_PASSWORD = env('POSTGRESQL_PASSWORD', default=None)
if POSTGRESQL_PASSWORD is None:
    raise ConfigError('POSTGRESQL_PASSWORD ERROR in env')
#
POSTGRESQL_DBNAME = env('POSTGRESQL_DBNAME', default=None)
if POSTGRESQL_DBNAME is None:
    raise ConfigError('POSTGRESQL_DBNAME ERROR in env')
#
# =====================================================
#
MINIO_USER = env('MINIO_USER', default=None)
if MINIO_USER is None:
    raise ConfigError('MINIO_USER ERROR in env')
#
MINIO_PASSWORD = env('MINIO_PASSWORD', default=None)
if MINIO_PASSWORD is None:
    raise ConfigError('MINIO_PASSWORD ERROR in env')
#
MINIO_HOST = env('MINIO_HOST', default=None)
if MINIO_HOST is None:
    raise ConfigError('MINIO_HOST ERROR in env')
#
MINIO_PORT = env('MINIO_PORT', default=None)
if MINIO_PORT is None:
    raise ConfigError('MINIO_PORT ERROR in env')
#
MINIO = f"{MINIO_HOST}:{MINIO_PORT}"
#
if env('MINIO_HTTPS', default='Off') in \
        ['on', 'On', 'ON', '1', 'True', 'TRUE', 'true']:
    MINIO_HTTPS = True
else:
    MINIO_HTTPS = False
#
MINIO_BUSKET_REC = env('MINIO_BUSKET_REC', default=None)
if MINIO_BUSKET_REC is None:
    raise ConfigError('MINIO_BUSKET_REC ERROR in env')
#
MINIO_TIMEOUT = env('MINIO_TIMEOUT', default=None)
if MINIO_TIMEOUT is None:
    raise ConfigError('MINIO_TIMEOUT ERROR in env')
if MINIO_TIMEOUT.isdigit():
    MINIO_TIMEOUT = int(MINIO_TIMEOUT)
else:
    raise ConfigError('MINIO_TIMEOUT NOT DIGIT')
#
# =====================================================
#
TTS_VOICE = env('TTS_VOICE', default=None)
if TTS_VOICE is None:
    raise ConfigError('TTS_VOICE ERROR in env')
#
# =====================================================
#
ASTERISK_HOST = env('ASTERISK_HOST', default=None)
if ASTERISK_HOST is None:
    raise ConfigError('ASTERISK_HOST ERROR in env')
#
ASTERISK_PORT = env('ASTERISK_PORT', default=None)
if ASTERISK_PORT.isdigit():
    ASTERISK_PORT = int(ASTERISK_PORT)
else:
    raise ConfigError('ASTERISK_PORT ERROR in env')
#
if env('ASTERICK_SSL', default='Off') in \
        ['on', 'On', 'ON', '1', 'True', 'TRUE', 'true']:
    ASTERICK_SSL = True
    HTTP = "https://"
else:
    ASTERICK_SSL = False
    HTTP = "http://"
#
ASTERISK_USERNAME = env('ASTERISK_USERNAME', default=None)
if ASTERISK_USERNAME is None:
    raise ConfigError('ASTERISK_USERNAME ERROR in env')
#
ASTERISK_PASSWORD = env('ASTERISK_PASSWORD', default=None)
if ASTERISK_PASSWORD is None:
    raise ConfigError('ASTERISK_PASSWORD ERROR in env')
#
ASTERICK_API_KEY = f"{ASTERISK_USERNAME}:{ASTERISK_PASSWORD}"
#
ASTERISK_OUT_CONTEXT = env('ASTERISK_OUT_CONTEXT', default=None)
if ASTERISK_OUT_CONTEXT is None:
    raise ConfigError('ASTERISK_OUT_CONTEXT ERROR in env')
#
ASTERISK_ENDPOINT = env('ASTERISK_ENDPOINT', default=None)
if ASTERISK_ENDPOINT is None:
    raise ConfigError('ASTERISK_ENDPOINT ERROR in env')
#
ASTERISK_URL = f"{HTTP}{ASTERISK_HOST}:{ASTERISK_PORT}{ASTERISK_ENDPOINT}"
#
ASTERISK_APPEND = env('ASTERISK_APPEND', default=None)
if ASTERISK_APPEND is None:
    raise ConfigError('ASTERISK_APPEND ERROR in env')
#
TMP_APPEND = '/{}@'
ASTERISK_APPEND = f'{ASTERISK_APPEND}{TMP_APPEND}{ASTERISK_OUT_CONTEXT}'
#
# =====================================================
#
ASTERISK_FTP_HOST = ASTERISK_HOST
#
ASTERISK_FTP_USERNAME = env('ASTERISK_FTP_USERNAME', default=None)
if ASTERISK_FTP_USERNAME is None:
    raise ConfigError('ASTERISK_FTP_USERNAME ERROR in env')
#
ASTERISK_FTP_PASSWORD = env('ASTERISK_FTP_PASSWORD', default=None)
if ASTERISK_FTP_PASSWORD is None:
    raise ConfigError('ASTERISK_FTP_PASSWORD ERROR in env')
#
# =====================================================
#
