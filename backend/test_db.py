import os
import sys

# 添加项目根目录到 Python 路径
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)

from backend.app import app
from backend.models.course import Course
from backend.config.database import db

def test_db():
    with app.app_context():
        try:
            # 测试数据库连接
            print("测试数据库连接...")
            db.engine.connect()
            print("数据库连接成功！")
            
            # 查询现有课程
            print("\n查询现有课程...")
            courses = Course.query.all()
            print(f"找到 {len(courses)} 个课程:")
            for course in courses:
                print(f"- {course.name}: {course.description}")
            
            # 测试添加新课程
            print("\n测试添加新课程...")
            test_course = Course(
                name="测试课程",
                description="这是一个测试课程"
            )
            db.session.add(test_course)
            db.session.commit()
            print("测试课程添加成功！")
            
            # 再次查询确认
            print("\n再次查询课程...")
            courses = Course.query.all()
            print(f"现在有 {len(courses)} 个课程:")
            for course in courses:
                print(f"- {course.name}: {course.description}")
                
        except Exception as e:
            print(f"测试失败: {str(e)}")
            import traceback
            print(f"错误堆栈: {traceback.format_exc()}")

if __name__ == '__main__':
    test_db() 