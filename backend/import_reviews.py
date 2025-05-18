import os
import sys
import json
from datetime import datetime
from sqlalchemy import create_engine, text
from dotenv import load_dotenv
from urllib.parse import quote_plus

# 添加项目根目录到 Python 路径
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)

# 加载环境变量
load_dotenv()

def get_db_uri():
    """获取数据库URI"""
    DB_HOST = os.getenv('DB_HOST', 'localhost')
    DB_PORT = os.getenv('DB_PORT', '3306')
    DB_USER = os.getenv('DB_USER', 'root')
    DB_PASSWORD = quote_plus(os.getenv('DB_PASSWORD', '350918'))
    DB_NAME = os.getenv('DB_NAME', 'duckstudy')
    return f'mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}'

def import_reviews():
    """导入课程评价数据"""
    json_file = os.path.join(BASE_DIR, 'frontend', 'data', 'course_reviews.json')
    
    try:
        # 读取 JSON 文件
        with open(json_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        print(f"成功读取评价数据文件: {json_file}")
        print(f"找到 {len(data['reviews'])} 条评价记录")
        
        # 创建数据库引擎
        engine = create_engine(get_db_uri())
        
        # 执行数据库操作
        with engine.connect() as conn:
            # 检查表结构
            result = conn.execute(text("DESCRIBE course_reviews"))
            columns = [row[0] for row in result]
            print("当前表结构:", columns)
            
            # 清空现有评价数据
            conn.execute(text('DELETE FROM course_reviews'))
            conn.commit()
            print("已清空现有评价数据")
            
            # 导入新数据
            for review_data in data['reviews']:
                # 查询 course_id
                course_result = conn.execute(
                    text("SELECT id FROM courses WHERE title = :title"),
                    {"title": review_data['course_name']}
                ).fetchone()
                if not course_result:
                    print(f"警告: 课程 '{review_data['course_name']}' 不存在，跳过")
                    continue
                course_id = course_result[0]
                
                # 查询 user_id
                user_result = conn.execute(
                    text("SELECT id FROM users WHERE username = :username"),
                    {"username": review_data['username']}
                ).fetchone()
                if not user_result:
                    print(f"警告: 用户 '{review_data['username']}' 不存在，跳过")
                    continue
                user_id = user_result[0]
                
                # 转换日期字符串为 datetime 对象
                created_at = review_data.get('created_at', datetime.now().strftime('%Y-%m-%d'))
                
                # 构建 SQL 语句和参数
                sql = '''
                INSERT INTO course_reviews (course_id, user_id, username, rating, content, created_at)
                VALUES (:course_id, :user_id, :username, :rating, :content, :created_at)
                '''
                params = {
                    'course_id': course_id,
                    'user_id': user_id,
                    'username': review_data['username'],
                    'rating': review_data['rating'],
                    'content': review_data['content'],
                    'created_at': created_at
                }
                conn.execute(text(sql), params)
                print(f"添加评价: 课程 {review_data['course_name']}, 评分 {review_data['rating']}")
                
                # 提交所有更改
                conn.commit()
                print("所有评价数据已成功导入")
            
    except Exception as e:
        print(f"导入评价数据失败: {str(e)}")
        import traceback
        print(f"错误堆栈: {traceback.format_exc()}")

if __name__ == '__main__':
    import_reviews() 