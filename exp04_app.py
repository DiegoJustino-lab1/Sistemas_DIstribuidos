import logging

# Por padrão o Logger do python é no-op
# Vamos usar um adaptador para usar o
# ZMQ PUB-SUB como logger (já possui classes prontas para isso)

# Obtém um logger para esta aplicação
logger = logging.getLogger(__name__)

# Uma função simples para utilizar o log
def world():
    logger.info('hello world!')