from app import app
from config.database import init_db, db
from models.post import Post
from models.user import User
from datetime import datetime

def init_posts():
    """初始化帖子数据"""
    # 初始化数据库
    init_db(app)
    
    with app.app_context():
        # 检查是否已有数据
        if Post.query.count() == 0:
            # 首先确保有用户数据
            if User.query.count() == 0:
                # 创建测试用户
                test_user = User(
                    username='test_user',
                    email='test@example.com'
                )
                test_user.set_password('password123')
                db.session.add(test_user)
                db.session.commit()
            
            # 获取测试用户
            test_user = User.query.filter_by(username='test_user').first()
            
            # 示例帖子数据
            sample_posts = [
                {
                    'user_id': test_user.id,
                    'content': '今天学习了Python的基础语法，感觉收获很大！',
                    'created_at': datetime.utcnow(),
                    'likes': 5
                },
                {
                    'user_id': test_user.id,
                    'content': '分享一个学习Web开发的好网站：https://www.w3school.com.cn',
                    'created_at': datetime.utcnow(),
                    'likes': 8
                },
                {
                    'user_id': test_user.id,
                    'content': '有人一起学习数据结构与算法吗？可以互相交流经验。',
                    'created_at': datetime.utcnow(),
                    'likes': 12
                }
            ]
            
            # 添加示例帖子
            for post_data in sample_posts:
                post = Post(**post_data)
                db.session.add(post)
            
            # 提交更改
            db.session.commit()
            print("示例帖子数据导入成功！")
        else:
            print("数据库中已有帖子数据，跳过导入。")

if __name__ == '__main__':
    init_posts() 