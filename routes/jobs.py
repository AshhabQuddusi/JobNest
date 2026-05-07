from flask import Blueprint, render_template, request, redirect, url_for, flash, abort
from flask_login import login_required, current_user
from extensions import db
from models.job import Job
from models.application import Application

jobs_bp = Blueprint('jobs', __name__)


@jobs_bp.route('/jobs')
def list_jobs():
    """Public job listing with search and filter."""
    query = request.args.get('q', '').strip()
    location = request.args.get('location', '').strip()
    job_type = request.args.get('job_type', '').strip()

    jobs_query = Job.query.filter_by(is_active=True)

    if query:
        jobs_query = jobs_query.filter(
            (Job.title.ilike(f'%{query}%')) |
            (Job.description.ilike(f'%{query}%')) |
            (Job.skills_required.ilike(f'%{query}%'))
        )

    if location:
        jobs_query = jobs_query.filter(Job.location.ilike(f'%{location}%'))

    if job_type:
        jobs_query = jobs_query.filter(Job.job_type == job_type)

    jobs = jobs_query.order_by(Job.created_at.desc()).all()

    # Collect which jobs the seeker has already applied to
    applied_job_ids = set()
    if current_user.is_authenticated and current_user.role == 'seeker':
        apps = Application.query.filter_by(user_id=current_user.id).all()
        applied_job_ids = {a.job_id for a in apps}

    return render_template(
        'jobs/list.html',
        jobs=jobs,
        applied_job_ids=applied_job_ids,
        query=query,
        location=location,
        job_type=job_type,
    )


@jobs_bp.route('/jobs/<int:job_id>')
def job_detail(job_id):
    job = Job.query.get_or_404(job_id)
    already_applied = False
    if current_user.is_authenticated and current_user.role == 'seeker':
        already_applied = Application.query.filter_by(
            job_id=job_id, user_id=current_user.id
        ).first() is not None
    return render_template('jobs/detail.html', job=job, already_applied=already_applied)
