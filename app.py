import os
from flask import Flask, render_template
from config import Config
from extensions import db, login_manager


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Ensure upload directory exists
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

    # Initialise extensions
    db.init_app(app)
    login_manager.init_app(app)

    # User loader for Flask-Login
    from models.user import User

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    # Register blueprints
    from routes.auth import auth_bp
    from routes.main import main_bp
    from routes.jobs import jobs_bp
    from routes.recruiter import recruiter_bp
    from routes.seeker import seeker_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(main_bp)
    app.register_blueprint(jobs_bp)
    app.register_blueprint(recruiter_bp)
    app.register_blueprint(seeker_bp)

    # Custom error pages
    @app.errorhandler(403)
    def forbidden(e):
        return render_template('errors/403.html'), 403

    @app.errorhandler(404)
    def not_found(e):
        return render_template('errors/404.html'), 404

    @app.errorhandler(500)
    def server_error(e):
        return render_template('errors/500.html'), 500

    # Create tables and demo data
    with app.app_context():
        db.create_all()

        from models.user import User
        from models.job import Job

        # Demo recruiter
        recruiter = User.query.filter_by(email='demo@JobNest.com').first()

        if not recruiter:
            recruiter = User(
                full_name='Demo Recruiter',
                email='demo@JobNest.com',
                password_hash='demo123',
                role='recruiter',
                company_name='TalentAI'
            )

            db.session.add(recruiter)
            db.session.commit()

        # Demo jobs
        if Job.query.count() == 0:

            demo_jobs = [

                Job(
                    title='Python Developer',
                    company='Google',
                    location='Delhi',
                    job_type='Full-time',
                    description='Develop Flask APIs and backend systems.',
                    requirements='Python, Flask, SQL',
                    salary_range='8-12 LPA',
                    skills_required='Python, Flask, MySQL',
                    recruiter_id=recruiter.id,
                    is_active=True
                ),

                Job(
                    title='Frontend Developer',
                    company='Microsoft',
                    location='Bangalore',
                    job_type='Full-time',
                    description='Build responsive frontend applications.',
                    requirements='HTML, CSS, JavaScript',
                    salary_range='6-10 LPA',
                    skills_required='HTML, CSS, JavaScript',
                    recruiter_id=recruiter.id,
                    is_active=True
                ),

                Job(
                    title='AI/ML Intern',
                    company='OpenAI Labs',
                    location='Remote',
                    job_type='Internship',
                    description='Work on NLP and machine learning models.',
                    requirements='Python, Machine Learning',
                    salary_range='25k/month',
                    skills_required='Python, NLP, scikit-learn',
                    recruiter_id=recruiter.id,
                    is_active=True
                ),

                Job(
                    title='Data Analyst',
                    company='Amazon',
                    location='Hyderabad',
                    job_type='Full-time',
                    description='Analyze business and customer data.',
                    requirements='SQL, Excel, Python',
                    salary_range='7-11 LPA',
                    skills_required='SQL, Python, Power BI',
                    recruiter_id=recruiter.id,
                    is_active=True
                )
            ]

            db.session.add_all(demo_jobs)
            db.session.commit()

            print('Demo jobs added successfully!')

    return app


app = create_app()

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)