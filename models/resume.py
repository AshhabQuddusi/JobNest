from extensions import db
from datetime import datetime


class Resume(db.Model):
    __tablename__ = 'resumes'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), nullable=False, index=True)
    filename = db.Column(db.String(255), nullable=False)       # stored filename on disk
    original_name = db.Column(db.String(255), nullable=False)  # original upload name
    extracted_text = db.Column(db.Text, nullable=True)         # full text from PDF
    extracted_skills = db.Column(db.Text, nullable=True)       # comma-separated identified skills
    uploaded_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationships
    applications = db.relationship('Application', backref='resume', lazy=True)

    def skills_list(self):
        """Return extracted skills as a Python list."""
        if self.extracted_skills:
            return [s.strip() for s in self.extracted_skills.split(',') if s.strip()]
        return []

    def __repr__(self):
        return f'<Resume {self.original_name} (user {self.user_id})>'
