from extensions import db
from datetime import datetime


class Application(db.Model):
    __tablename__ = 'applications'

    id = db.Column(db.Integer, primary_key=True)
    job_id = db.Column(db.Integer, db.ForeignKey('jobs.id', ondelete='CASCADE'), nullable=False, index=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), nullable=False, index=True)
    resume_id = db.Column(db.Integer, db.ForeignKey('resumes.id', ondelete='SET NULL'), nullable=True)

    cover_letter = db.Column(db.Text, nullable=True)

    # Similarity score computed by ranking engine (0.0 – 1.0)
    similarity_score = db.Column(db.Float, default=0.0)

    status = db.Column(
        db.Enum('pending', 'reviewed', 'shortlisted', 'rejected'),
        default='pending'
    )
    applied_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Unique constraint: one application per user per job
    __table_args__ = (
        db.UniqueConstraint('job_id', 'user_id', name='uq_job_user'),
    )

    def __repr__(self):
        return f'<Application job={self.job_id} user={self.user_id} score={self.similarity_score:.3f}>'
