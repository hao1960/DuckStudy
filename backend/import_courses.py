import os
import sys
import json
from datetime import datetime
from sqlalchemy import text
from db_config import get_engine

# 添加项目根目录到 Python 路径
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)

def import_courses():
    """导入课程数据"""
    try:
        # 读取课程数据文件
        courses_file = os.path.join(BASE_DIR, 'frontend', 'data', 'courses.json')
        with open(courses_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
            courses_data = data['courses']
        print(f"成功读取课程数据文件: {courses_file}")
        print(f"找到 {len(courses_data)} 条课程记录")
        
        # 创建数据库引擎
        engine = get_engine()
        
        # 执行数据库操作
        with engine.connect() as conn:
            # 清空现有课程数据
            conn.execute(text('DELETE FROM course_reviews'))
            conn.execute(text('DELETE FROM courses'))
            conn.commit()
            print("已清空现有课程数据")
            
            # 导入新数据
            for course_data in courses_data:
                # 准备课程数据
                sql = '''
                INSERT INTO courses (
                    title, description, cover_image, price, average_rating,
                    teacher, department, category, campus, credits, hours,
                    semester, location, created_at, updated_at
                ) VALUES (
                    :title, :description, :cover_image, :price, :average_rating,
                    :teacher, :department, :category, :campus, :credits, :hours,
                    :semester, :location, :created_at, :updated_at
                )
                '''
                params = {
                    'title': course_data['name'],
                    'description': course_data['description'],
                    'cover_image': f"https://example.com/{course_data['name']}.jpg",
                    'price': 0.0,
                    'average_rating': 0.0,
                    'teacher': course_data['teacher'],
                    'department': course_data['department'],
                    'category': course_data['category'],
                    'campus': course_data['campus'],
                    'credits': course_data['credits'],
                    'hours': course_data['hours'],
                    'semester': course_data['semester'],
                    'location': course_data['location'],
                    'created_at': datetime.now(),
                    'updated_at': datetime.now()
                }
                
                # 执行插入
                conn.execute(text(sql), params)
                print(f"添加课程: {course_data['name']}")
            
            conn.commit()
            print("课程数据导入成功！")
            
    except Exception as e:
        print(f"导入课程数据失败: {str(e)}")
        import traceback
        print(f"错误堆栈: {traceback.format_exc()}")

if __name__ == '__main__':
    import_courses() 