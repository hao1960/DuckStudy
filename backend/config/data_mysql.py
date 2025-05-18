import pymysql

conn = pymysql.connect(
    host = 'localhost',
    user = 'root',
    password = '350918',
    db  = 'test',
    port = 3306,
    charset = 'utf8'
)
#游标
