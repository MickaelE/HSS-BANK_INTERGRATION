from global_logger import Log

log = Log.get_logger()
log.verbose = True
log = Log.get_logger(logs_dir='logs')
