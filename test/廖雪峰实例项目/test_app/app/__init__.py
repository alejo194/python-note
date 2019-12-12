import logging
import logging.handlers

# LOG_FILE = './log/server_info.log'
#
# handler = logging.handlers.RotatingFileHandler(LOG_FILE, maxBytes=1024*1024)
# fmt = '%(asctime)s - %(filename)s:%(lineno)s - %(name)s - %(message)s'
#
# formatter = logging.Formatter(fmt)
# handler.setFormatter(formatter)
#
# logger = logging.getLogger('server_info')
# logger.addHandler(handler)
# logger.setLevel(logging.INFO)

logger = logging.getLogger()
formatter = logging.Formatter('%(asctime)s %(name)-12s %(levelname)-8s %(message)s')
logger.setLevel(logging.INFO)
consoleHandler = logging.StreamHandler()
consoleHandler.setFormatter(formatter)
logger.addHandler(consoleHandler)
