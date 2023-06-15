import sys
import datetime


class Logger(object):
    def __init__(self, filename="Default.log"):
        current_datetime = datetime.datetime.now()
        timestamp = current_datetime.strftime("%Y%m%d_%H%M%S")
        filename_with_timestamp = f"{timestamp}_{filename}"
        self.terminal = sys.stdout
        self.log = open(filename_with_timestamp, "a")

    def write(self, message):
        self.terminal.write(message)
        self.log.write(message)

    def flush(self):
        pass
