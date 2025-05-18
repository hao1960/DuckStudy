from config.database import db
from datetime import datetime

class CourseReview(db.Model):
    """课程评价模型"""
    __tablename__ = 'course_reviews'
    __table_args__ = {'extend_existing': True}
    
    id = db.Column(db.Integer, primary_key=True)
    course_id = db.Column(db.Integer, db.ForeignKey('courses.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    username = db.Column(db.String(50), nullable=False)
    rating = db.Column(db.Float, nullable=False)
    content = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f'<CourseReview {self.id}>'
    
    def to_dict(self):
        """转换为字典格式"""
        return {
            'id': self.id,
            'course_id': self.course_id,
            'user_id': self.user_id,
            'username': self.username,
            'rating': self.rating,
            'content': self.content,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        } 