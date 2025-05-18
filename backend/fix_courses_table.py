import os
import sys
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)

from sqlalchemy import create_engine, text
from dotenv import load_dotenv
from urllib.parse import quote_plus

# 加载环境变量
load_dotenv()

def get_db_uri():
    """获取数据库URI"""
    DB_HOST = os.getenv('DB_HOST', 'localhost')
    DB_PORT = os.getenv('DB_PORT', '3306')
    DB_USER = os.getenv('DB_USER', 'root')
    DB_PASSWORD = quote_plus(os.getenv('DB_PASSWORD', '350918'))
    DB_NAME = os.getenv('DB_NAME', 'duckstudy')
    return f'mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}'

def fix_courses_table():
    # 创建数据库引擎
    engine = create_engine(get_db_uri())
    
    # 执行数据库操作
    with engine.connect() as conn:
        # 删除旧表
        conn.execute(text('DROP TABLE IF EXISTS course_reviews'))
        conn.execute(text('DROP TABLE IF EXISTS courses'))
        conn.commit()
        
        # 创建新表
        conn.execute(text('''
        CREATE TABLE courses (
            id INT AUTO_INCREMENT PRIMARY KEY,
            title VARCHAR(255) NOT NULL,
            description TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
        )
        '''))
        conn.commit()
        print("表结构修复成功")

if __name__ == '__main__':
    fix_courses_table() 