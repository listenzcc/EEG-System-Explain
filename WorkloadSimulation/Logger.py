import logging


fmt = '%(asctime)s %(name)s %(levelname)-8s %(message)-40s {{%(filename)s:%(lineno)s}}'

logger = logging.getLogger('WorkloadSimulation')
logger.setLevel(logging.DEBUG)

console_handler = logging.StreamHandler()
console_handler.setFormatter(logging.Formatter(fmt))
console_handler.setLevel(logging.DEBUG)

logger.addHandler(console_handler)
