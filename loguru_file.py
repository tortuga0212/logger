from loguru import logger

logger.add('byte_log.json',
           format='{time} {level} {name} {function} {line} {message}',
           level='DEBUG',
           rotation='64 MB',
           compression='zip',
           serialize=True
)

logger.add('time.log',
           format='{time} {level} {name} {function} {line} {message}',
           level='DEBUG',
           rotation='1 week',
           compression='zip'
)

logger.add('error.log',
           format='{time} {level} {name} {function} {line} {message}',
           level='ERROR'
)

logger.debug('this is debug')
logger.info('this is info')
logger.warning('this is warning')
logger.error('this is error')
logger.critical('this is critical')