
import os
import time


class Logger:
    LOGGING_FILE_DIR = os.path.join(os.path.dirname(__file__), 'logs')
    LOGGING_FILE_PATH_FORMAT = os.path.join(LOGGING_FILE_DIR, 'log__{timestamp}.log')

    def __init__(self):
        if not os.path.exists(Logger.LOGGING_FILE_DIR):
            os.mkdir(Logger.LOGGING_FILE_DIR)

        self.__log_file_name = \
            Logger.LOGGING_FILE_PATH_FORMAT.format(timestamp=time.strftime('%d_%m_%Y__%H_%M_%S'))
        self.log('Logger created', should_print=True)

    def error(self, msg):
        self.log('ERROR: {msg}'.format(msg=msg))

    def log(self, msg, should_print=True):
        formatter_msg = '[{timestamp}] >> {msg}'.format(timestamp=time.strftime('%d/%m/%Y %H:%M:%S'), msg=msg)
        with open(self.__log_file_name, 'ab') as log_file:
            log_file.write('{msg}\n'.format(msg=formatter_msg))

        if should_print:
            self.print_msg(msg)

    def print_msg(self, msg):
        print msg


