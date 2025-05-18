import os
import sys
from flask import Flask
from dotenv import load_dotenv
from urllib.parse import quote_plus
from sqlalchemy import text

# 添加项目根目录到 Python 路径
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)

# 加载环境变量
load_dotenv()

from backend.config.database import db, get_db_uri

def recreate_tables():
    """重新创建数据库表"""
    try:
        # 创建新的 Flask 应用实例
        app = Flask(__name__)
        app.config['SQLALCHEMY_DATABASE_URI'] = get_db_uri()
        app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
        app.config['SQLALCHEMY_ECHO'] = True
        
        # 初始化数据库
        db.init_app(app)
        
        with app.app_context():
            # 使用原生 SQL 删除表
            db.session.execute(text("DROP TABLE IF EXISTS course_reviews"))
            db.session.execute(text("DROP TABLE IF EXISTS courses"))
            db.session.commit()
            print("已删除所有表")
            
            # 使用原生 SQL 创建表
            create_courses_table = """
            CREATE TABLE courses (
                id INT AUTO_INCREMENT PRIMARY KEY,
                title VARCHAR(100) NOT NULL,
                description TEXT,
                cover_image VARCHAR(200),
                price FLOAT DEFAULT 0.0,
                average_rating FLOAT DEFAULT 0.0,
                teacher VARCHAR(50),
                department VARCHAR(50),
                category VARCHAR(20),
                campus VARCHAR(50),
                credits INT,
                hours INT,
                semester VARCHAR(50),
                location VARCHAR(100),
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
            )
            """
            
            create_course_reviews_table = """
            CREATE TABLE course_reviews (
                id INT AUTO_INCREMENT PRIMARY KEY,
                course_id INT NOT NULL,
                user_id INT NOT NULL,
                username VARCHAR(50) NOT NULL,
                rating FLOAT NOT NULL,
                content TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
                FOREIGN KEY (course_id) REFERENCES courses(id)
            )
            """
            
            # 执行创建表的 SQL
            db.session.execute(text(create_courses_table))
            db.session.execute(text(create_course_reviews_table))
            db.session.commit()
            print("已重新创建所有表")
            
            # 验证表结构
            result = db.session.execute(text("DESCRIBE courses"))
            print("\n验证 courses 表结构:")
            for row in result:
                print(f"字段: {row[0]}, 类型: {row[1]}, 允许空: {row[2]}, 键: {row[3]}, 默认值: {row[4]}, 额外: {row[5]}")
            
    except Exception as e:
        print(f"重新创建表失败: {str(e)}")
        import traceback
        print(f"错误堆栈: {traceback.format_exc()}")

if __name__ == '__main__':
    recreate_tables() 