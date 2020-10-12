import logging
import os
LOG_PATH='/var/log/lvanops/access.log'
LOG_LEVEL='DEBUG'
LOG_FORMAT='%(levelname)s - %(asctime)s - %(name)s - %(module)s - %(message)s'
def get_logger(name=None):
    logger=logging.getLogger(name)
    logger.setLevel(LOG_LEVEL)
    log_path=os.path.dirname(LOG_PATH)
    if not os.path.exists(log_path):
        os.makedirs(log_path)
    file_handler=logging.FileHandler(LOG_PATH)
    file_handler.setLevel(level=LOG_LEVEL)
    formatter=logging.Formatter(LOG_FORMAT)
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
    return logger
