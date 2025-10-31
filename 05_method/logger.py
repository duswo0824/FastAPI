import logging

class Logger():

    logging.basicConfig(
        level=logging.INFO,
        format='%(levelname)s: [%(name)s] %(message)s - %(asctime)s',
        datefmt='%H:%M:%S',
    )

    def get_logger(self,name):
        return logging.getLogger(name)
