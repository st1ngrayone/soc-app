import os


class Config:
    DEBUG = True
    SECRET_KEY = os.getenv('SECRET_KEY', 'APPSECRETKEY!')
    MYSQL_HOST = os.getenv('MYSQL_HOST', '192.168.88.100')
    MYSQL_USER = os.getenv('MYSQL_USER', 'monty')
    MYSQL_PASSWORD = os.getenv('MYSQL_PASSWORD', 'debian1')
    MYSQL_DB = os.getenv('MYSQL_DB', 'socapp')
    REDIS_HOST = os.getenv('REDIS_HOST', '192.168.88.100')
    REDIS_DB = os.getenv('REDIS_DB', 1)
    REDIS_URL = os.getenv('REDIS_URL')
    RMQ_URL = os.getenv('RMQ_URL', 'amqp://guest:guest@srv1.lan:5672/%2f')

