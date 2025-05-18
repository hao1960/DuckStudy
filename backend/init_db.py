import os
import sys

# 添加项目根目录到 Python 路径
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)

from backend.app import app
from backend.config.database import init_db, db
from backend.models import User, Post, Course

def init_database():
    """初始化数据库和表"""
    # 初始化数据库
    init_db(app)
    print("数据库初始化完成！")

if __name__ == '__main__':
    init_database() 