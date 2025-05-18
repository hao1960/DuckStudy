import os
import sys

# 添加项目根目录到 Python 路径
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)

from backend.app import app
from backend.utils.course_importer import import_course_data

def test_import():
    with app.app_context():
        json_file = os.path.join(BASE_DIR, 'frontend', 'data', 'courses.json')
        print(f"尝试导入文件: {json_file}")
        if import_course_data(json_file):
            print('课程数据导入成功！')
        else:
            print('课程数据导入失败！')

if __name__ == '__main__':
    test_import() 