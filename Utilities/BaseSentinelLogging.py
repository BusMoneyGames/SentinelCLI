# coding=utf-8
import logging


class MyFormatter(logging.Formatter):

    """
    Custom logging formatter found here
    https://stackoverflow.com/questions/1343227/can-pythons-logging-format-be-modified-depending-on-the-message-log-level

    """

    default_fmt = logging.Formatter('%(levelname)s (asctime)s - %(message)s')
    debug_fmt = logging.Formatter('%(levelname)s - [%(filename)s:%(lineno)s] - %(funcName)s - %(message)s')
    info_fmt = logging.Formatter('%(asctime)s %(levelname)s - %(message)s')

    def format(self, record):
        if record.levelno == logging.INFO:
            return self.info_fmt.format(record)
        elif record.levelno == logging.DEBUG:
            return self.debug_fmt.format(record)
        else:
            return self.default_fmt.format(record)

# Creating a new logger
root_logger = logging.getLogger()

# Adding the stream handler
ch = logging.StreamHandler()
# Creating the new custom formatter
fm = MyFormatter()
ch.setFormatter(fm)

# Adding the handler and setting the default logging level
root_logger.addHandler(ch)
root_logger.setLevel(logging.INFO)
