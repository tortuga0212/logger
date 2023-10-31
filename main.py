import logging, zipfile, os, datetime
from logging.handlers import RotatingFileHandler, TimedRotatingFileHandler


logger = logging.getLogger()
# FORMAT = '%(levelname)s (%(asctime)s): %(message)s (Line: %(lineno)d) [%(filename)s]'
FORMAT = '[%(asctime)s]|<%(levelname)-7s>|: [%(name)s].[%(funcName)s.py:%(lineno)d]:> %(message)s'
logger.setLevel(logging.DEBUG)

st_hand = logging.StreamHandler()
st_hand.setFormatter(logging.Formatter(FORMAT))
st_hand.setLevel(logging.DEBUG)

# def get_log_filename(filename):
#     log_directory = os.path.split(filename)[0]
#     date = os.path.splitext(filename)[1][1:]
#     filename = os.path.join(log_directory, date)

if not os.path.exists('log_file'):
    os.makedirs('log_file')
fl_hand_byte = logging.handlers.RotatingFileHandler(
    filename='./log_file/log_file_byte.log', mode='a', maxBytes=64000000, backupCount=30, encoding='utf-8', delay=False,
    errors=None
    )
fl_hand_time = logging.handlers.TimedRotatingFileHandler(
    filename='./log_file/log_file_time.log', when='W0', interval=1, backupCount=30, encoding='utf-8', delay=False,
    utc=False,atTime=None, errors=None
)
fl_hand_byte.setFormatter(logging.Formatter(FORMAT))
fl_hand_time.setFormatter(logging.Formatter(FORMAT))
fl_hand_byte.setLevel(logging.DEBUG)
fl_hand_time.setLevel(logging.DEBUG)

#creating a monthly archive log_file.zip
x = datetime.datetime.now()
if x.day == 29:
    file_zip = zipfile.ZipFile(f'./log_file/log_file_{x.month}.zip', 'w')
    for folder, subfolders, files in os.walk('log_file'):
        for file in files:
            if file.endswith('.log'):
                file_zip.write(os.path.join(folder, file),
                               os.path.relpath(os.path.join(folder, file), 'log_file'),
                               compress_type=zipfile. ZIP_DEFLATED)
file_zip.close()

#creating an archive for the year log_file.zip
if x.day == 29 and x.month == 10:
    file_zip = zipfile.ZipFile(f'./log_file/log_file_{x.year}.zip', 'w')
    for folder, subfolders, files in os.walk('log_file'):
        for file in files:
            if file.endswith('.zip'):
                file_zip.write(os.path.join(folder, file),
                               os.path.relpath(os.path.join(folder, file), 'log_file'),
                               compress_type=zipfile.ZIP_DEFLATED)
file_zip.close()

if not os.path.exists('error_file'):
    os.makedirs('error_file')
er_hand = logging.FileHandler(filename='./error_file/error_file.log')
er_hand.setFormatter(logging.Formatter(FORMAT))
er_hand.setLevel(logging.ERROR)

#creating a monthly archive error_file.zip
if x.day == 29:
    file_zip = zipfile.ZipFile(f'./error_file/error_file_{x.month}.zip', 'w')
    for folder, subfolders, files in os.walk('error_file'):
        for file in files:
            if file.endswith('.log'):
                file_zip.write(os.path.join(folder, file),
                               os.path.relpath(os.path.join(folder, file), 'error_file'),
                               compress_type=zipfile.ZIP_DEFLATED)
file_zip.close()

#creating an archive for the year error_file.zip
if x.day == 29 and x.month == 10:
    file_zip = zipfile.ZipFile(f'./error_file/error_file_{x.year}.zip', 'w')
    for folder, subfolders, files in os.walk('error_file'):
        for file in files:
            if file.endswith('.zip'):
                file_zip.write(os.path.join(folder, file),
                               os.path.relpath(os.path.join(folder, file), 'error_file'),
                               compress_type=zipfile.ZIP_DEFLATED)
file_zip.close()


logger.addHandler(st_hand)
logger.addHandler(fl_hand_byte)
logger.addHandler(fl_hand_time)
logger.addHandler(er_hand)

logger.info('initialized')
logger.error('this is error')

fl_hand_byte.close()
fl_hand_time.close()
er_hand.close()

if x.day == 29:
    dir1 = './log_file'
    for f in os.listdir(dir1):
        if f.endswith('.log'):
            os.remove(os.path.join(dir1, f))
    dir2 = './error_file'
    for f in os.listdir(dir2):
        if f.endswith('.log'):
            os.remove(os.path.join(dir2, f))


if x.day == 29 and x.month == 10:
    dir3 = './log_file'
    for f in os.listdir(dir3):
        if f.endswith('.zip'):
            os.remove(os.path.join(dir3, f))
    dir4 = './error_file'
    for f in os.listdir(dir4):
        if f.endswith('.zip'):
            os.remove(os.path.join(dir4, f))