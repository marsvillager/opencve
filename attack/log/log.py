import re
import sys
import datetime


class Logger(object):
    def __init__(self, filename="log"):
        current_datetime = datetime.datetime.now()
        timestamp = current_datetime.strftime("%Y%m%d_%H%M%S")
        filename_with_timestamp = f"{filename}{timestamp}.txt"
        self.terminal = sys.stdout
        self.log = open(filename_with_timestamp, "a")

    def write(self, message):
        self.terminal.write(message)
        message = re.sub('\033\[[0-9;]+m', '', message)  # 使用正则表达式去除颜色代码
        self.log.write(message)

    def flush(self):
        pass
