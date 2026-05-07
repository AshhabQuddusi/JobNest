from flask import Blueprint, render_template, request, redirect, url_for, flash, abort
from flask_login import login_required, current_user
from extensions import db
from models.job import Job
from models.application import Application
from models.resume import Resume
from utils.helpers import save_uploaded_file, delete_file_if_exists, get_upload_path
from utils.resume_parser import parse_resume

seeker_bp = Blueprint('seeker', __name__, url_prefix='/seeker')


def require_seeker():
    if not current_user.is_authenticated or current_user.role != 'seeker':
        abort(403)


# ─── Dashboard ────────────────────────────────────────────────────────────────

@seeker_bp.route('/dashboard')
@login_required
def dashboard():
    require_seeker()
    applications = (
        Application.query
        .filter_by(user_id=current_user.id)
        .order_by(Application.applied_at.desc())
        .all()
    )
    resumes = Resume.query.filter_by(user_id=current_user.id).all()
    return render_template('seeker/dashboard.html',
                           applications=applications,
                           resumes=resumes)


# ─── Upload Resume ────────────────────────────────────────────────────────────

@seeker_bp.route('/resume/upload', methods=['GET', 'POST'])
@login_required
def upload_resume():
    require_seeker()

    if request.method == 'POST':
        file = request.files.get('resume_file')

        try:
            unique_name = save_uploaded_file(file)
        except ValueError as e:
            flash(str(e), 'danger')
            return redirect(request.url)

        # Parse text and skills from the uploaded PDF
        filepath = get_upload_path(unique_name)
        parsed = parse_resume(filepath)

        resume = Resume(
            user_id=current_user.id,
            filename=unique_name,
            original_name=file.filename,
            extracted_text=parsed['text'],
            extracted_skills=', '.join(parsed['skills']),
        )
        db.session.add(resume)
        db.session.commit()

        flash('Resume uploaded and parsed successfully!', 'success')
        return redirect(url_for('seeker.dashboard'))

    return render_template('seeker/upload_resume.html')


# ─── Delete Resume ────────────────────────────────────────────────────────────

@seeker_bp.route('/resume/<int:resume_id>/delete', methods=['POST'])
@login_required
def delete_resume(resume_id):
    require_seeker()
    resume = Resume.query.get_or_404(resume_id)

    if resume.user_id != current_user.id:
        abort(403)

    delete_file_if_exists(resume.filename)
    db.session.delete(resume)
    db.session.commit()
    flash('Resume deleted.', 'info')
    return redirect(url_for('seeker.dashboard'))


# ─── Apply for a Job ──────────────────────────────────────────────────────────

@seeker_bp.route('/apply/<int:job_id>', methods=['GET', 'POST'])
@login_required
def apply(job_id):
    require_seeker()
    job = Job.query.get_or_404(job_id)

    # Prevent duplicate applications
    existing = Application.query.filter_by(
        job_id=job_id, user_id=current_user.id
    ).first()
    if existing:
        flash('You have already applied for this job.', 'warning')
        return redirect(url_for('jobs.job_detail', job_id=job_id))

    resumes = Resume.query.filter_by(user_id=current_user.id).all()
    if not resumes:
        flash('Please upload a resume before applying.', 'warning')
        return redirect(url_for('seeker.upload_resume'))

    if request.method == 'POST':
        resume_id = request.form.get('resume_id', type=int)
        cover_letter = request.form.get('cover_letter', '').strip()

        resume = Resume.query.get(resume_id)
        if not resume or resume.user_id != current_user.id:
            flash('Invalid resume selected.', 'danger')
            return render_template('seeker/apply.html', job=job, resumes=resumes)

        application = Application(
            job_id=job_id,
            user_id=current_user.id,
            resume_id=resume_id,
            cover_letter=cover_letter,
            similarity_score=0.0,  # computed lazily when recruiter views applicants
            status='pending',
        )
        db.session.add(application)
        db.session.commit()

        flash('Application submitted successfully!', 'success')
        return redirect(url_for('seeker.dashboard'))

    return render_template('seeker/apply.html', job=job, resumes=resumes)


# ─── Withdraw Application ─────────────────────────────────────────────────────

@seeker_bp.route('/application/<int:app_id>/withdraw', methods=['POST'])
@login_required
def withdraw(app_id):
    require_seeker()
    app = Application.query.get_or_404(app_id)

    if app.user_id != current_user.id:
        abort(403)

    db.session.delete(app)
    db.session.commit()
    flash('Application withdrawn.', 'info')
    return redirect(url_for('seeker.dashboard'))
