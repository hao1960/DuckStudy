from flask_sqlalchemy import SQLAlchemy
from flask import Flask
import os
from dotenv import load_dotenv
from urllib.parse import quote_plus

# 加载环境变量
load_dotenv()

# 创建数据库实例
db = SQLAlchemy()

def get_db_uri():
    """获取数据库URI"""
    DB_HOST = os.getenv('DB_HOST', 'localhost')
    DB_PORT = os.getenv('DB_PORT', '3306')
    DB_USER = os.getenv('DB_USER', 'root')
    DB_PASSWORD = quote_plus(os.getenv('DB_PASSWORD', '350918'))
    DB_NAME = os.getenv('DB_NAME', 'duckstudy')
    return f'mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}'

def init_db(app: Flask) -> None:
    """初始化数据库"""
    if not isinstance(app, Flask):
        raise TypeError("app must be an instance of Flask")
    
    # 配置数据库
    app.config['SQLALCHEMY_DATABASE_URI'] = get_db_uri()
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SQLALCHEMY_ECHO'] = True  # 启用SQL语句日志
    
    # 初始化数据库
    db.init_app(app)
    
    # 创建所有表
    with app.app_context():
        try:
            db.create_all()
            print(f"MySQL数据库连接成功: {get_db_uri()}")
        except Exception as e:
            print(f"数据库初始化失败: {str(e)}")
            raise

# 确保只初始化一次
_initialized = False

def ensure_db_initialized(app: Flask) -> None:
    """确保数据库只初始化一次"""
    global _initialized
    if not _initialized:
        init_db(app)
        _initialized = True 