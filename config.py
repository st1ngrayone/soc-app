class Config:
    DEBUG = True
    SECRET_KEY = 'APPSECRETKEY1!'
    MYSQL_HOST = '192.168.88.100'
    MYSQL_USER = 'monty'
    MYSQL_PASSWORD = 'debian1'
    MYSQL_DB = 'socapp'

class ConfigFake:
    host = '192.168.88.100'
    user = "monty"
    password = "debian1"
    database = "socapp"