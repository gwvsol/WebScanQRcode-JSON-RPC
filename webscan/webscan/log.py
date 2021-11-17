# import logging
from loguru import logger as logging

# log_format = '%(asctime)s.%(msecs)d|\
# %(levelname)s|%(module)s.%(funcName)s:%(lineno)d %(message)s'
# logging.basicConfig(level=logging.INFO,
#                     format=log_format,
#                     datefmt='%Y-%m-%d %H:%M:%S')

logging.add(str, format="<green>{time:YYYY-MM-DD HH:mm:ss}</green>|\
{level}|<cyan>{name}</cyan>:<cyan>{function}\
</cyan>:<cyan>{line}</cyan> {message}")
