from flask import Blueprint, render_template, request, redirect, url_for, flash, abort, send_from_directory
from flask_login import login_required, current_user
from extensions import db
from models.job import Job
from models.application import Application
from models.resume import Resume
from utils.ranking import rank_resumes, build_job_corpus_text
from config import Config

recruiter_bp = Blueprint('recruiter', __name__, url_prefix='/recruiter')


def require_recruiter():
    """Abort with 403 if the current user is not a recruiter."""
    if not current_user.is_authenticated or current_user.role != 'recruiter':
        abort(403)


# ─── Dashboard ────────────────────────────────────────────────────────────────

@recruiter_bp.route('/dashboard')
@login_required
def dashboard():
    require_recruiter()
    jobs = Job.query.filter_by(recruiter_id=current_user.id).order_by(Job.created_at.desc()).all()

    # Build stats
    total_applications = sum(
        Application.query.filter_by(job_id=j.id).count() for j in jobs
    )
    return render_template(
        'recruiter/dashboard.html',
        jobs=jobs,
        total_applications=total_applications,
    )


# ─── Post Job ─────────────────────────────────────────────────────────────────

@recruiter_bp.route('/post-job', methods=['GET', 'POST'])
@login_required
def post_job():
    require_recruiter()

    if request.method == 'POST':
        title = request.form.get('title', '').strip()
        company = request.form.get('company', current_user.company_name or '').strip()
        location = request.form.get('location', '').strip()
        job_type = request.form.get('job_type', 'Full-time')
        description = request.form.get('description', '').strip()
        requirements = request.form.get('requirements', '').strip()
        salary_range = request.form.get('salary_range', '').strip()
        skills_required = request.form.get('skills_required', '').strip()

        if not title or not description or not requirements:
            flash('Title, description, and requirements are required.', 'danger')
            return render_template('recruiter/post_job.html')

        job = Job(
            title=title,
            company=company,
            location=location,
            job_type=job_type,
            description=description,
            requirements=requirements,
            salary_range=salary_range,
            skills_required=skills_required,
            recruiter_id=current_user.id,
        )
        db.session.add(job)
        db.session.commit()

        flash('Job posted successfully!', 'success')
        return redirect(url_for('recruiter.dashboard'))

    return render_template('recruiter/post_job.html',
                           company=current_user.company_name or '')


# ─── Edit Job ─────────────────────────────────────────────────────────────────

@recruiter_bp.route('/job/<int:job_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_job(job_id):
    require_recruiter()
    job = Job.query.get_or_404(job_id)

    if job.recruiter_id != current_user.id:
        abort(403)

    if request.method == 'POST':
        job.title = request.form.get('title', job.title).strip()
        job.company = request.form.get('company', job.company).strip()
        job.location = request.form.get('location', job.location).strip()
        job.job_type = request.form.get('job_type', job.job_type)
        job.description = request.form.get('description', job.description).strip()
        job.requirements = request.form.get('requirements', job.requirements).strip()
        job.salary_range = request.form.get('salary_range', job.salary_range).strip()
        job.skills_required = request.form.get('skills_required', job.skills_required or '').strip()
        job.is_active = 'is_active' in request.form

        db.session.commit()
        flash('Job updated successfully.', 'success')
        return redirect(url_for('recruiter.dashboard'))

    return render_template('recruiter/post_job.html', job=job, company=job.company)


# ─── Delete Job ───────────────────────────────────────────────────────────────

@recruiter_bp.route('/job/<int:job_id>/delete', methods=['POST'])
@login_required
def delete_job(job_id):
    require_recruiter()
    job = Job.query.get_or_404(job_id)

    if job.recruiter_id != current_user.id:
        abort(403)

    db.session.delete(job)
    db.session.commit()
    flash('Job deleted.', 'info')
    return redirect(url_for('recruiter.dashboard'))


# ─── View Applicants with Ranking ─────────────────────────────────────────────

@recruiter_bp.route('/job/<int:job_id>/applicants')
@login_required
def view_applicants(job_id):
    require_recruiter()
    job = Job.query.get_or_404(job_id)

    if job.recruiter_id != current_user.id:
        abort(403)

    applications = Application.query.filter_by(job_id=job_id).all()

    # Build corpus for ranking from resumes linked to applications
    resume_corpus = []
    for app in applications:
        resume = Resume.query.get(app.resume_id) if app.resume_id else None
        text = resume.extracted_text if resume else ''
        resume_corpus.append({'id': app.id, 'text': text or ''})

    # Run TF-IDF ranking
    job_text = build_job_corpus_text(job)
    ranked = rank_resumes(job_text, resume_corpus)

    # Build a map: application_id → score, rank
    score_map = {r['id']: {'score': r['score'], 'rank': idx + 1}
                 for idx, r in enumerate(ranked)}

    # Update similarity scores in DB for persistence
    for app in applications:
        if app.id in score_map:
            app.similarity_score = score_map[app.id]['score']
    db.session.commit()

    # Attach ranking data to applications for template
    ranked_applications = sorted(
        applications,
        key=lambda a: score_map.get(a.id, {}).get('score', 0),
        reverse=True,
    )

    return render_template(
        'recruiter/applicants.html',
        job=job,
        applications=ranked_applications,
        score_map=score_map,
    )


# ─── Update Application Status ────────────────────────────────────────────────

@recruiter_bp.route('/application/<int:app_id>/status', methods=['POST'])
@login_required
def update_status(app_id):
    require_recruiter()
    application = Application.query.get_or_404(app_id)
    job = Job.query.get_or_404(application.job_id)

    if job.recruiter_id != current_user.id:
        abort(403)

    new_status = request.form.get('status')
    if new_status in ('pending', 'reviewed', 'shortlisted', 'rejected'):
        application.status = new_status
        db.session.commit()
        flash(f'Application status updated to "{new_status}".', 'success')

    return redirect(url_for('recruiter.view_applicants', job_id=job.id))


# ─── Download Resume ──────────────────────────────────────────────────────────

@recruiter_bp.route('/resume/<int:resume_id>/download')
@login_required
def download_resume(resume_id):
    require_recruiter()
    resume = Resume.query.get_or_404(resume_id)
    return send_from_directory(
        Config.UPLOAD_FOLDER,
        resume.filename,
        as_attachment=True,
        download_name=resume.original_name,
    )
