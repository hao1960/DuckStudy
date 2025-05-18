import os
import sys
import json
from datetime import datetime
from sqlalchemy import create_engine, text
from dotenv import load_dotenv
from urllib.parse import quote_plus
import hashlib

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

def hash_password(password):
    """对密码进行哈希处理"""
    return hashlib.sha256(password.encode()).hexdigest()

def import_users():
    """导入用户数据"""
    json_file = os.path.join(BASE_DIR, 'frontend', 'data', 'users.json')
    
    try:
        # 读取 JSON 文件
        with open(json_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        print(f"成功读取用户数据文件: {json_file}")
        print(f"找到 {len(data['users'])} 条用户记录")
        
        # 创建数据库引擎
        engine = create_engine(get_db_uri())
        
        # 执行数据库操作
        with engine.connect() as conn:
            # 检查表结构
            result = conn.execute(text("DESCRIBE users"))
            columns = [row[0] for row in result]
            print("当前表结构:", columns)
            
                # 清空现有用户数据
            conn.execute(text('DELETE FROM users'))
            conn.commit()
                print("已清空现有用户数据")
                
                # 导入新数据
                for user_data in data['users']:
                # 准备用户数据
                username = user_data['username']
                password_hash = hash_password(user_data['password'])
                email = user_data.get('email', '')
                avatar = user_data.get('avatar', 'https://placehold.jp/40x40.png')
                role = user_data.get('role', 'user')
                
                # 构建 SQL 语句和参数
                sql = '''
                INSERT INTO users (username, password_hash, email, avatar, role)
                VALUES (:username, :password_hash, :email, :avatar, :role)
                '''
                params = {
                    'username': username,
                    'password_hash': password_hash,
                    'email': email,
                    'avatar': avatar,
                    'role': role
                }
                
                # 执行插入
                conn.execute(text(sql), params)
                print(f"添加用户: {username}")
                
                # 提交所有更改
            conn.commit()
                print("所有用户数据已成功导入")
            
    except Exception as e:
        print(f"导入用户数据失败: {str(e)}")
        import traceback
        print(f"错误堆栈: {traceback.format_exc()}")

if __name__ == '__main__':
    import_users() 