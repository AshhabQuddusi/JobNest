from extensions import db
from datetime import datetime


class Job(db.Model):
    __tablename__ = 'jobs'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    company = db.Column(db.String(150), nullable=False)
    location = db.Column(db.String(150), nullable=False)
    job_type = db.Column(db.Enum('Full-time', 'Part-time', 'Contract', 'Internship', 'Remote'), default='Full-time')
    description = db.Column(db.Text, nullable=False)
    requirements = db.Column(db.Text, nullable=False)
    salary_range = db.Column(db.String(100), nullable=True)
    skills_required = db.Column(db.Text, nullable=True)  # comma-separated

    # Foreign key linking to recruiter user
    recruiter_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), nullable=False, index=True)

    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationships
    applications = db.relationship('Application', backref='job', lazy=True, cascade='all, delete-orphan')

    def skills_list(self):
        """Return skills as a Python list."""
        if self.skills_required:
            return [s.strip() for s in self.skills_required.split(',') if s.strip()]
        return []

    def __repr__(self):
        return f'<Job {self.title} at {self.company}>'
