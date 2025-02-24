import logging
import sys

logger = logging.getLogger('logger')
logger.setLevel(logging.INFO)

handler = logging.StreamHandler(sys.stdout)
handler.setFormatter(logging.Formatter(fmt='[%(asctime)s %(filename)s:%(funcName)s %(levelname)s] %(message)s'))
logger.addHandler(handler)