"""Database models for the village portal."""

from app import db
from datetime import datetime


class Problem(db.Model):
    """Model for storing villager problems/complaints."""
    
    __tablename__ = 'problems'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    category = db.Column(db.String(50), nullable=False)
    description = db.Column(db.Text, nullable=False)
    contact = db.Column(db.String(120), nullable=False)
    status = db.Column(db.String(20), default='New')  # New, In Progress, Resolved
    submitted_to_jansunwai = db.Column(db.Boolean, default=False)
    jansunwai_link = db.Column(db.String(255), nullable=True)  # Link to Jansunwai complaint
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<Problem {self.id}: {self.name} - {self.category}>'
    
    def to_dict(self):
        """Convert problem to dictionary for JSON serialization."""
        return {
            'id': self.id,
            'name': self.name,
            'category': self.category,
            'description': self.description,
            'contact': self.contact,
            'status': self.status,
            'submitted_to_jansunwai': self.submitted_to_jansunwai,
            'jansunwai_link': self.jansunwai_link,
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M:%S')
        }
