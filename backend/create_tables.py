import os
import sys
from flask import Flask
from config.database import db, init_db
from models import User, Post, Comment, Course, CourseReview
from dotenv import load_dotenv

# 添加项目根目录到 Python 路径
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)

# 加载环境变量
load_dotenv()

# 获取数据库 URI
DB_URI = os.getenv('SQLALCHEMY_DATABASE_URI', 'mysql+pymysql://root:350918@localhost:3306/duckstudy')

def create_tables():
    """创建所有数据库表"""
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = DB_URI
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    init_db(app)
    with app.app_context():
        db.create_all()
        print("所有表已成功创建")

if __name__ == '__main__':
    create_tables() 