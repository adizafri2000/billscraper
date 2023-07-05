import logging

import utilities

log_format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
LOGGER_NAME = "mainlogger"
#log_format = '[%(asctime)s] %(message)s'
'''
logger.basicConfig(
    level=logging.DEBUG,
    filename=utilities.generate_log_file_name(),
    format=log_format,
    filemode='w'
)
'''
'''
def setup_logger(logger_name):
    logger = logging.getLogger(logger_name)
    logger.setLevel(logging.INFO)

    # create file handler which logs even debug messages
    now = datetime.now()
    log_folder = "logs"
    if not os.path.exists(log_folder):
        print("Dedicated log directory not found. Creating new directory logs/")
        os.mkdir(log_folder)
    os.chdir(log_folder)
    logfile = now.strftime("%Y%m%d-%H%M%S") + ".log"

    fh = logging.FileHandler(logfile)
    fh.setLevel(logging.INFO)
    # create console handler with a higher log level
    ch = logging.StreamHandler()
    ch.setLevel(logging.INFO)
    # create formatter and add it to the handlers
    formatter = logging.Formatter(log_format)
    fh.setFormatter(formatter)
    ch.setFormatter(formatter)
    # add the handlers to the logger
    logger.addHandler(fh)
    logger.addHandler(ch)
    return logger
'''

def setup_logger():
    logger = logging
    logger.basicConfig(
        level=logging.DEBUG,
        format=log_format,
        #filemode='w',
        handlers=[
            logger.FileHandler(utilities.generate_log_file_name()),
            logger.StreamHandler()
        ]
   )
    return logger

logger = setup_logger()