import os
import sys

# 添加项目根目录到 Python 路径
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)

from backend.app import app
from backend.models.course import Course
from backend.config.database import db
import json

def manual_import():
    with app.app_context():
        # 读取JSON文件
        json_file = os.path.join(BASE_DIR, 'frontend', 'data', 'courses.json')
        with open(json_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        # 打印 Course 模型的属性
        print("Course 模型的属性:")
        for attr in dir(Course):
            if not attr.startswith('_'):
                print(f"- {attr}")
        
        # 插入数据
        for course_data in data.get('courses', []):
            try:
                print(f"\n尝试创建课程，数据: {course_data}")
                course = Course(
                    name=course_data['title'],
                    description=course_data.get('description', '')
                )
                db.session.add(course)
                print(f"添加课程: {course.name}")
            except Exception as e:
                print(f"添加课程失败: {str(e)}")
                print(f"错误类型: {type(e)}")
                import traceback
                print(f"错误堆栈: {traceback.format_exc()}")
        
        try:
            db.session.commit()
            print("数据导入成功！")
        except Exception as e:
            db.session.rollback()
            print(f"提交失败: {str(e)}")

if __name__ == '__main__':
    manual_import() 