# backend/models/course.py
from datetime import datetime
from config.database import db

class Course(db.Model):
    """课程模型"""
    __tablename__ = 'courses'
    __table_args__ = {'extend_existing': True}
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    cover_image = db.Column(db.String(200))
    price = db.Column(db.Float, default=0.0)
    average_rating = db.Column(db.Float, default=0.0)
    teacher = db.Column(db.String(50))
    department = db.Column(db.String(50))
    category = db.Column(db.String(20))
    campus = db.Column(db.String(50))
    credits = db.Column(db.Integer)
    hours = db.Column(db.Integer)
    semester = db.Column(db.String(50))
    location = db.Column(db.String(100))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # 关联关系
    reviews = db.relationship('CourseReview', 
                            backref=db.backref('course', lazy=True), 
                            lazy=True)
    
    def update_average_rating(self):
        """更新课程均分"""
        if self.reviews:
            self.average_rating = sum(review.rating for review in self.reviews) / len(self.reviews)
        else:
            self.average_rating = 0.0
    
    def __repr__(self):
        return f'<Course {self.title}>'