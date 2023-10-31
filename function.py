import logging, zipfile, os, datetime
from logging.handlers import RotatingFileHandler, TimedRotatingFileHandler

logger = logging.getLogger(__name__)
logging.getLogger('aiogram').addHandler(logging.StreamHandler())
logging.getLogger('uvicorn').addHandler(logging.StreamHandler())
logging.getLogger('fastapi').addHandler(logging.StreamHandler())
logging.getLogger('aiohttp').addHandler(logging.StreamHandler())
FORMAT = '[%(asctime)s]|<%(levelname)-7s>|: [%(name)s].[%(funcName)s.py:%(lineno)d]:> %(message)s'
logger.setLevel(logging.DEBUG)

if not os.path.exists('log_file'):
    os.makedirs('log_file')

if not os.path.exists('error_file'):
    os.makedirs('error_file')

x = datetime.datetime.now()

class ColoredFormatter(logging.Formatter):
    """Special custom formatter for colorizing log messages!"""
    RED = '\033[0;31m'
    GREEN = '\033[0;32m'
    BLUE = '\033[0;34m'
    PURPLE = '\033[0;35m'
    YELLOW = '\033[1;33m'
    RESET = "\033[0m"

    def __init__(self, *args, **kwargs):
        self._colors = {logging.DEBUG: self.PURPLE,
                        logging.INFO: self.GREEN,
                        logging.WARNING: self.YELLOW,
                        logging.ERROR: self.BLUE,
                        logging.CRITICAL: self.RED}
        super(ColoredFormatter, self).__init__(*args, **kwargs)

    def format(self, record):
        """Applies the color formats"""
        # record.msg = self._colors[record.levelno] + record.msg + self.RESET
        record.msg = self._colors[record.levelno] + record.msg + self.RESET
        return logging.Formatter.format(self, record)

    def setLevelColor(self, logging_level, escaped_ansi_code):
        self._colors[logging_level] = escaped_ansi_code

def stream_handler():
    st_hand = logging.StreamHandler()
    st_hand.setLevel(logging.DEBUG)
    st_hand.setFormatter(ColoredFormatter(FORMAT))
    logger.addHandler(st_hand)
    return st_hand

def file_handler_byte():
    global fl_hand_byte
    fl_hand_byte = logging.handlers.RotatingFileHandler(
        filename='./log_file/log_file_byte.log', maxBytes=64000000, backupCount=30, encoding='utf-8')
    fl_hand_byte.setLevel(logging.DEBUG)
    fl_hand_byte.setFormatter(logging.Formatter(FORMAT))
    logger.addHandler(fl_hand_byte)
    return fl_hand_byte

def file_handler_time():
    global fl_hand_time
    fl_hand_time = logging.handlers.TimedRotatingFileHandler(
        filename='./log_file/log_file_time.log', when='W0', interval=1, backupCount=30, encoding='utf-8')
    fl_hand_time.setFormatter(logging.Formatter(FORMAT))
    fl_hand_time.setLevel(logging.DEBUG)
    logger.addHandler(fl_hand_time)
    return fl_hand_time

def error_handler():
    global er_hand
    er_hand = logging.FileHandler(filename='./error_file/error_file.log')
    er_hand.setFormatter(logging.Formatter(FORMAT))
    er_hand.setLevel(logging.ERROR)
    logger.addHandler(er_hand)
    return er_hand

def archive_month_log():
    if x.day == 1:
        file_zip = zipfile.ZipFile(f'./log_file/{x.month}.zip', 'w')
        for folder, subfolders, files in os.walk('log_file'):
            for file in files:
                if file.endswith('.log'):
                    file_zip.write(os.path.join(folder, file),
                                   os.path.relpath(os.path.join(folder, file), 'log_file'),
                                   compress_type=zipfile.ZIP_DEFLATED)
        file_zip.close()

def archive_month_error():
    if x.day == 1:
        file_zip = zipfile.ZipFile(f'./error_file/{x.month}.zip', 'w')
        for folder, subfolders, files in os.walk('error_file'):
            for file in files:
                if file.endswith('.log'):
                    file_zip.write(os.path.join(folder, file),
                                   os.path.relpath(os.path.join(folder, file), 'error_file'),
                                   compress_type=zipfile.ZIP_DEFLATED)
        file_zip.close()

def archive_year_log():
    if x.day == 1 and x.month == 1:
        file_zip = zipfile.ZipFile(f'./log_file/log_file_{x.year - 1}.zip', 'w')
        for folder, subfolders, files in os.walk('log_file'):
            for file in files:
                num = 1
                while num != 13:
                    if file == f'{num}.zip':
                        file_zip.write(os.path.join(folder, file),
                                       os.path.relpath(os.path.join(folder, file), 'log_file'),
                                       compress_type=zipfile.ZIP_DEFLATED)
                        break
                    num += 1
        file_zip.close()

def archive_year_error():
    if x.day == 1 and x.month == 1:
        file_zip = zipfile.ZipFile(f'./error_file/error_file_{x.year}.zip', 'w')
        for folder, subfolders, files in os.walk('error_file'):
            for file in files:
                num = 1
                while num != 13:
                    if file == f'{num}.zip':
                        file_zip.write(os.path.join(folder, file),
                                       os.path.relpath(os.path.join(folder, file), 'error_file'),
                                       compress_type=zipfile.ZIP_DEFLATED)
                        break
                    num += 1
        file_zip.close()

def delete_old_files():
    fl_hand_byte.close()
    fl_hand_time.close()
    er_hand.close()
    if x.day == 1:
        dir1 = './log_file'
        for f in os.listdir(dir1):
            if f.endswith('.log'):
                os.remove(os.path.join(dir1, f))

        dir2 = './error_file'
        for f in os.listdir(dir2):
            if f.endswith('.log'):
                os.remove(os.path.join(dir2, f))

def delete_old_zip():
    if x.day == 1 and x.month == 1:
        for folder, subfolders, files in os.walk('log_file'):
            for file in files:
                num = 1
                while num != 13:
                    if file == f'{num}.zip':
                        os.remove(os.path.join('log_file', file))
                        break
                    num += 1

        for folder, subfolders, files in os.walk('error_file'):
            for file in files:
                num = 1
                while num != 13:
                    if file == f'{num}.zip':
                        os.remove(os.path.join('error_file', file))
                        break
                    num += 1


def test():
    logger.info('initialized')
    logger.info('this is info')
    logger.debug('this is debug')
    logger.warning('this is warning')
    logger.error('this is error')
    logger.critical('this is critical')

def main():
    return stream_handler(), file_handler_byte(), file_handler_time(), error_handler(), archive_month_log(), \
        archive_month_error(), archive_year_log(), delete_old_zip(), archive_year_error()

if __name__ == '__main__':
    main()
    test()
    delete_old_files()

