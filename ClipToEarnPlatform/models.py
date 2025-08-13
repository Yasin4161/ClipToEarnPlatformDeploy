from app import db
from flask_login import UserMixin
from datetime import datetime

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Payment information
    full_name = db.Column(db.String(100))
    iban = db.Column(db.String(256))  # Encrypted IBAN needs more space
    
    # KVKK/GDPR Compliance
    consent_given = db.Column(db.Boolean, default=False)
    consent_date = db.Column(db.DateTime)
    consent_ip = db.Column(db.String(45))
    
    # İlişkiler
    clips = db.relationship('Clip', backref='clipper', lazy=True)
    
    def __repr__(self):
        return f'<User {self.username}>'

class StreamTask(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    stream_url = db.Column(db.String(500), nullable=False)
    reward_per_1k_views = db.Column(db.Float, nullable=False, default=0.75)
    deadline = db.Column(db.DateTime, nullable=False)
    description = db.Column(db.Text)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    created_by = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    
    # İlişkiler
    clips = db.relationship('Clip', backref='task', lazy=True)
    
    def __repr__(self):
        return f'<StreamTask {self.title}>'

class Clip(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    clip_url = db.Column(db.String(500), nullable=False)
    platform = db.Column(db.String(50), nullable=False)  # 'youtube' or 'tiktok'
    description = db.Column(db.Text)
    view_count = db.Column(db.Integer, default=0)
    earnings = db.Column(db.Float, default=0.0)
    is_paid = db.Column(db.Boolean, default=False)
    status = db.Column(db.String(20), default='pending')  # pending, approved, rejected
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Foreign keys
    clipper_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    task_id = db.Column(db.Integer, db.ForeignKey('stream_task.id'), nullable=False)
    
    def calculate_earnings(self):
        if self.view_count > 0:
            self.earnings = (self.view_count / 1000) * self.task.reward_per_1k_views
        else:
            self.earnings = 0.0
    
    def __repr__(self):
        return f'<Clip {self.id} - {self.platform}>'
