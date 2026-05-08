# JobNest — AI-Powered Recruitment Platform

JobNest is a full-stack, AI-powered recruitment platform built with Flask and MySQL that intelligently ranks job applicants using TF-IDF and cosine-similarity-based resume-job matching.

---

## 🚀 Features

### 👨‍💼 Job Seekers
- Secure registration and login system
- Upload PDF resumes
- Browse and search job listings
- Apply to jobs with resumes and cover letters
- View application status and AI match scores
- Withdraw applications anytime

### 🏢 Recruiters
- Create and manage job postings
- View AI-ranked applicants
- Access uploaded resumes
- Shortlist or reject candidates
- Manage recruitment workflow efficiently

### 🤖 AI Resume Ranking
- Extracts text from uploaded PDF resumes
- Uses TF-IDF vectorisation for document analysis
- Computes cosine similarity between resumes and job descriptions
- Automatically ranks applicants by relevance score

---

## 🛠 Tech Stack

- Python 3.11
- Flask
- Flask-SQLAlchemy
- MySQL
- Scikit-learn
- pdfplumber
- HTML5
- CSS3
- JavaScript

---

## 📸 Screenshots

| Home Page | Jobs Dashboard | Recruiter Panel 
* | <img width="1915" height="924" alt="Screenshot 2026-05-08 151110" src="https://github.com/user-attachments/assets/41ac05c3-794d-40c6-9db7-f88eb3b05da5" />

* | *<img width="1906" height="912" alt="Screenshot 2026-05-08 151140" src="https://github.com/user-attachments/assets/f71e4a6f-935f-4274-8f74-62abb22a9f3b" />
* | *<img width="1904" height="914" alt="Screenshot 2026-05-08 151154" src="https://github.com/user-attachments/assets/ebf52d90-ced9-4da5-865e-43c6dbcd969d" />
  | Jobs Dashboard |
* | *<img width="1906" height="922" alt="Screenshot 2026-05-08 151250" src="https://github.com/user-attachments/assets/1d54d934-55ce-41e0-9f9d-7bfdfbaf9e0d" />
  | AI Applicant Ranking |
* | <img width="1893" height="913" alt="Screenshot 2026-05-08 151238" src="https://github.com/user-attachments/assets/dda985f2-5752-40c1-bf1a-32d7f85a5821" />


---

## 📁 Project Structure

```bash
project_root/
│
├── app.py
├── config.py
├── database.sql
├── requirements.txt
│
├── models/
├── routes/
├── templates/
├── static/
├── utils/
└── uploads/

⚙️ Installation & Setup
1. Clone Repository
git clone https://github.com/AshhabQuddusi/JobNest.git
cd JobNest
2. Create Virtual Environment
python -m venv venv

Activate virtual environment:

Windows
venv\Scripts\activate
Linux/macOS
source venv/bin/activate
3. Install Dependencies
pip install -r requirements.txt
4. Configure Environment Variables

Create a .env file in the root directory:

SECRET_KEY=your_secret_key

DB_HOST=localhost
DB_PORT=3306
DB_USER=root
DB_PASSWORD=your_mysql_password
DB_NAME=job_portal

5. Set up MySQL Database
CREATE DATABASE job_portal;

Import schema: mysql -u root -p job_portal < database.sql

6. Run Application
python app.py

Open browser: http://localhost:5000

🧠 How AI Ranking Works
Recruiters post job descriptions and requirements
Job seekers upload resumes in PDF format
Resume text is extracted using pdfplumber
TF-IDF vectorisation converts text into numerical vectors
Cosine similarity calculates resume-job relevance
Applicants are ranked automatically based on similarity scores

🔒 Security Features
Password hashing using Werkzeug
Secure file upload handling
Role-based access control
SQLAlchemy ORM protection against SQL injection
Environment variable configuration support

🚀 Highlights
AI-powered applicant ranking
Resume parsing with PDF text extraction
Recruiter and seeker dashboards
Machine learning integration
Flask backend architecture
MySQL relational database design

📌 Project Status
JobNest is a portfolio and academic project demonstrating AI-assisted recruitment workflows using Flask, MySQL, and machine learning techniques.

👨‍💻 Developer
Ashhab Quddusi
LinkedIn: linkedin.com/in/ashhab-quddusi/
Email: ashhabquddusi4@gmail.com

📄 License
This project is developed for educational and portfolio purposes.
