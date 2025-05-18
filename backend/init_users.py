import os
import sys
from datetime import datetime

# 添加项目根目录到Python路径
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)

import backend.models  # 注册所有模型
from backend.app import app
from backend.models import User
from backend.config.database import db
from werkzeug.security import generate_password_hash

def init_users():
    """初始化用户数据"""
    with app.app_context():
        # 不要再调用init_db(app)，只用db
        if User.query.count() > 0:
            print("用户数据已存在，跳过初始化")
            return
        # 创建示例用户
        users = [
            {
                'username': 'admin',
                'email': 'admin@example.com',
                'password': 'admin123',
                'role': 'admin',
                'avatar': 'https://placehold.jp/40x40.png'
            },
            {
                'username': 'user1',
                'email': 'user1@example.com',
                'password': 'user123',
                'role': 'user',
                'avatar': 'https://placehold.jp/40x40.png'
            }
        ]
        # 添加用户到数据库
        for user_data in users:
            user = User(
                username=user_data['username'],
                email=user_data['email'],
                role=user_data['role'],
                avatar=user_data['avatar']
            )
            user.set_password(user_data['password'])
            db.session.add(user)
        try:
            db.session.commit()
            print("用户数据初始化成功")
        except Exception as e:
            db.session.rollback()
            print(f"初始化用户数据时出错: {str(e)}")

if __name__ == '__main__':
    init_users() 