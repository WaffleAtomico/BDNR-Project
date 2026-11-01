from app.logger.const import CRITICAL, ERROR, INFO, DEBUG, WARNING
from app.utils.get_current_time import TimeUtils

class Logger:
    def info(self, message):
        print(f"{INFO}: [{TimeUtils.get_current_time()}] {message}")
    def debug(self, message):
        print(f"{DEBUG}: [{TimeUtils.get_current_time()}] {message}")
    def warning(self, message):
        print(f"{WARNING}: [{TimeUtils.get_current_time()}] {message}")
    def critical(self, message):
        print(f"{CRITICAL}: [{TimeUtils.get_current_time()}] {message}")
    def error(self, message):
        print(f"{ERROR}: [{TimeUtils.get_current_time()}] {message}")
