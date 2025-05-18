import os
import sys

# 添加项目根目录到 Python 路径
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)

from backend.app import app
from backend.config.database import db
from sqlalchemy import text

def check_table():
    with app.app_context():
        try:
            # 获取表结构
            with db.engine.connect() as conn:
                # 检查courses表结构
                result = conn.execute(text("PRAGMA table_info(courses)"))
                print("\nCourses表结构:")
                for row in result:
                    print(f"列名: {row[1]}, 类型: {row[2]}, 是否可空: {row[3]}, 默认值: {row[4]}")
                
                # 检查course_reviews表结构
                result = conn.execute(text("PRAGMA table_info(course_reviews)"))
                print("\nCourse_reviews表结构:")
                for row in result:
                    print(f"列名: {row[1]}, 类型: {row[2]}, 是否可空: {row[3]}, 默认值: {row[4]}")
                
        except Exception as e:
            print(f"检查表结构失败: {str(e)}")
            import traceback
            print(f"错误堆栈: {traceback.format_exc()}")

if __name__ == '__main__':
    check_table() 