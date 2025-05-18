import os
from sqlalchemy import create_engine
from dotenv import load_dotenv
from urllib.parse import quote_plus

# 添加项目根目录到 Python 路径
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# 加载环境变量
load_dotenv()

def get_db_uri():
    """获取数据库URI，优先使用 MySQL，如果不可用则使用 SQLite"""
    try:
        # 尝试使用 MySQL
        DB_HOST = os.getenv('DB_HOST', 'localhost')
        DB_PORT = os.getenv('DB_PORT', '3306')
        DB_USER = os.getenv('DB_USER', 'root')
        DB_PASSWORD = quote_plus(os.getenv('DB_PASSWORD', '350918'))
        DB_NAME = os.getenv('DB_NAME', 'duckstudy')
        mysql_uri = f'mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}'
        
        # 测试 MySQL 连接
        engine = create_engine(mysql_uri)
        with engine.connect() as conn:
            conn.execute("SELECT 1")
        print("使用 MySQL 数据库")
        return mysql_uri
    except Exception as e:
        # MySQL 连接失败，使用 SQLite
        sqlite_path = os.path.join(BASE_DIR, 'data', 'duckstudy.db')
        os.makedirs(os.path.dirname(sqlite_path), exist_ok=True)
        sqlite_uri = f'sqlite:///{sqlite_path}'
        print(f"MySQL 连接失败: {str(e)}")
        print(f"使用 SQLite 数据库: {sqlite_path}")
        return sqlite_uri

def get_engine():
    """获取数据库引擎"""
    return create_engine(get_db_uri()) 