import sys


class LogRecorder(object):
    def __init__(self, file_name="./log.txt"):
        self.terminal = sys.stdout
        self.log = open(file_name, "w", encoding='utf-8')

    def write(self, message):
        self.terminal.write(message)
        self.log.write(message)

    def flush(self):
        pass
