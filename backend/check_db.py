import os
import sys
from flask import Flask
from dotenv import load_dotenv
from urllib.parse import quote_plus
from sqlalchemy import text

# 添加项目根目录到 Python 路径
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)

# 加载环境变量
load_dotenv()

from backend.config.database import db, get_db_uri

def check_db():
    """检查数据库表结构"""
    try:
        # 创建新的 Flask 应用实例
        app = Flask(__name__)
        app.config['SQLALCHEMY_DATABASE_URI'] = get_db_uri()
        app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
        app.config['SQLALCHEMY_ECHO'] = True
        
        # 初始化数据库
        db.init_app(app)
        
        with app.app_context():
            # 检查 courses 表结构
            result = db.session.execute(text("DESCRIBE courses"))
            print("\n当前 courses 表结构:")
            for row in result:
                print(f"字段: {row[0]}, 类型: {row[1]}, 允许空: {row[2]}, 键: {row[3]}, 默认值: {row[4]}, 额外: {row[5]}")
            
    except Exception as e:
        print(f"检查数据库失败: {str(e)}")
        import traceback
        print(f"错误堆栈: {traceback.format_exc()}")

if __name__ == '__main__':
    check_db() 