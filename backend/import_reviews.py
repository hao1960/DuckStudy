import os
import sys
import json
from datetime import datetime
from sqlalchemy import text
from db_config import get_engine

# 添加项目根目录到 Python 路径
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)

def import_reviews():
    """导入课程评价数据"""
    try:
        # 读取评价数据文件
        reviews_file = os.path.join(BASE_DIR, 'frontend', 'data', 'course_reviews.json')
        with open(reviews_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
            reviews_data = data['reviews']
        print(f"成功读取评价数据文件: {reviews_file}")
        print(f"找到 {len(reviews_data)} 条评价记录")
        
        # 创建数据库引擎
        engine = get_engine()
        
        # 执行数据库操作
        with engine.connect() as conn:
            # 获取当前表结构
            result = conn.execute(text("DESCRIBE course_reviews"))
            columns = [row[0] for row in result]
            print(f"当前表结构: {columns}")
            
            # 清空现有评价数据
            conn.execute(text('DELETE FROM course_reviews'))
            conn.commit()
            print("已清空现有评价数据")
            
            # 导入新数据
            for review_data in reviews_data:
                # 获取课程ID
                result = conn.execute(
                    text("SELECT id FROM courses WHERE title = :title"),
                    {"title": review_data['course_name']}
                )
                course = result.fetchone()
                
                if not course:
                    print(f"警告: 课程 '{review_data['course_name']}' 不存在，跳过")
                    continue
                
                # 准备评价数据
                sql = '''
                INSERT INTO course_reviews (
                    course_id, user_id, username, rating, content,
                    created_at, updated_at
                ) VALUES (
                    :course_id, :user_id, :username, :rating, :content,
                    :created_at, :updated_at
                )
                '''
                params = {
                    'course_id': course[0],
                    'user_id': review_data['user_id'],
                    'username': review_data['username'],
                    'rating': review_data['rating'],
                    'content': review_data['content'],
                    'created_at': datetime.now(),
                    'updated_at': datetime.now()
                }
                
                # 执行插入
                conn.execute(text(sql), params)
                print(f"添加评价: 课程 {review_data['course_name']}, 评分 {review_data['rating']}")
            
            conn.commit()
            print("所有评价数据已成功导入")
            
    except Exception as e:
        print(f"导入评价数据失败: {str(e)}")
        import traceback
        print(f"错误堆栈: {traceback.format_exc()}")

if __name__ == '__main__':
    import_reviews() 