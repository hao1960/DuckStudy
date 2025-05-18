import os
import sys

# 添加项目根目录到 Python 路径
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)

from backend.app import app
from backend.models.course import Course

def check_model():
    with app.app_context():
        print("Course 模型的属性:")
        for attr in dir(Course):
            if not attr.startswith('_'):
                print(f"- {attr}")
        
        print("\nCourse 模型的列:")
        for column in Course.__table__.columns:
            print(f"- {column.name}: {column.type}")

if __name__ == '__main__':
    check_model() 