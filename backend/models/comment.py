from config.database import db
from datetime import datetime

class Comment(db.Model):
    """评论模型"""
    __tablename__ = 'comments'
    __table_args__ = {'extend_existing': True}
    
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey('posts.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # 关联关系
    post = db.relationship('backend.models.post.Post', 
                         backref=db.backref('comments', lazy=True), 
                         lazy=True)
    
    def __repr__(self):
        return f'<Comment {self.id}>' 