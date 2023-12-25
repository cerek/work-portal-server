from decouple import config

if config('DB_ENGINE') == 'mysql':
    import pymysql
    pymysql.install_as_MySQLdb()