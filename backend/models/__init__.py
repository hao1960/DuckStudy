from config.database import db
from .course import Course
from .user import User
from .course_review import CourseReview
from .post import Post
from .comment import Comment

# 确保所有模型都被导入
__all__ = ['User', 'Post', 'Comment', 'Course', 'CourseReview']

def init_models():
    """初始化所有模型"""
    pass  # 所有模型已经在上面导入 