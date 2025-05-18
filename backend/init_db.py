import os
import sys
from sqlalchemy import text
from db_config import get_engine

# 添加项目根目录到 Python 路径
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)

def init_db():
    """初始化数据库表结构"""
    try:
        # 创建数据库引擎
        engine = get_engine()
        
        # 执行数据库操作
        with engine.connect() as conn:
            # 创建课程表
            conn.execute(text('''
            CREATE TABLE IF NOT EXISTS courses (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title VARCHAR(100) NOT NULL,
                description TEXT,
                cover_image VARCHAR(200),
                price DECIMAL(10,2) DEFAULT 0.0,
                average_rating DECIMAL(3,2) DEFAULT 0.0,
                teacher VARCHAR(50),
                department VARCHAR(50),
                category VARCHAR(50),
                campus VARCHAR(50),
                credits INTEGER,
                hours INTEGER,
                semester VARCHAR(20),
                location VARCHAR(50),
                created_at DATETIME,
                updated_at DATETIME
            )
            '''))
            
            # 创建课程评价表
            conn.execute(text('''
            CREATE TABLE IF NOT EXISTS course_reviews (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                course_id INTEGER NOT NULL,
                user_id INTEGER NOT NULL,
                username VARCHAR(50) NOT NULL,
                rating INTEGER NOT NULL,
                content TEXT,
                created_at DATETIME,
                updated_at DATETIME,
                FOREIGN KEY (course_id) REFERENCES courses (id)
            )
            '''))
            
            conn.commit()
            print("数据库表结构初始化成功！")
            
    except Exception as e:
        print(f"初始化数据库失败: {str(e)}")
        import traceback
        print(f"错误堆栈: {traceback.format_exc()}")

if __name__ == '__main__':
    init_db() 