import os
import sys
from datetime import datetime

# 添加项目根目录到 Python 路径
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)

from backend.app import app
from backend.config.database import db, init_db
from backend.models import User, Course, CourseReview
from werkzeug.security import generate_password_hash

def init_sample_data():
    """初始化示例数据"""
    # 确保数据库已初始化
    init_db(app)
    
    with app.app_context():
        # 检查是否已有数据
        if User.query.count() > 0:
            print("数据库中已有数据，跳过初始化")
            return

        # 创建示例用户
        users = [
            User(
                username='admin',
                email='admin@example.com',
                password_hash=generate_password_hash('admin123'),
                role='admin',
                created_at=datetime.utcnow()
            ),
            User(
                username='test_user',
                email='test@example.com',
                password_hash=generate_password_hash('test123'),
                role='user',
                created_at=datetime.utcnow()
            )
        ]

        # 添加用户
        for user in users:
            db.session.add(user)
        db.session.commit()
        print("示例用户数据导入成功！")

        # 创建示例课程
        courses = [
            Course(
                name='Python基础教程',
                description='适合初学者的Python入门课程，包含基础语法、数据类型、控制流程等内容。',
                created_at=datetime.utcnow()
            ),
            Course(
                name='Web开发入门',
                description='HTML, CSS, JavaScript基础教程，帮助你快速入门Web开发。',
                created_at=datetime.utcnow()
            ),
            Course(
                name='数据结构与算法',
                description='系统学习常用数据结构和算法，提高编程能力。',
                created_at=datetime.utcnow()
            )
        ]

        # 添加课程
        for course in courses:
            db.session.add(course)
        db.session.commit()
        print("示例课程数据导入成功！")

        # 创建示例课程评价
        reviews = [
            CourseReview(
                course_id=1,  # Python基础教程
                user_id=2,    # test_user
                rating=5,
                content='课程内容非常系统，讲解清晰，适合初学者。',
                created_at=datetime.utcnow()
            ),
            CourseReview(
                course_id=1,  # Python基础教程
                user_id=1,    # admin
                rating=4,
                content='整体不错，但希望能增加更多实践项目。',
                created_at=datetime.utcnow()
            ),
            CourseReview(
                course_id=2,  # Web开发入门
                user_id=2,    # test_user
                rating=5,
                content='课程循序渐进，实例丰富，收获很大。',
                created_at=datetime.utcnow()
            )
        ]

        # 添加课程评价
        for review in reviews:
            db.session.add(review)
        db.session.commit()
        print("示例课程评价数据导入成功！")

        # 更新课程平均评分
        for course in courses:
            course.update_average_rating()
        db.session.commit()
        print("课程平均评分更新成功！")

if __name__ == '__main__':
    init_sample_data() 