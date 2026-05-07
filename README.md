# JobNest — AI-Powered Recruitment Platform

> JobNest is a full-stack AI-powered recruitment platform built with Flask and MySQL that intelligently ranks job applicants using TF-IDF and cosine similarity based resume-job matching.

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
- Uses TF-IDF vectorization for document analysis
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

| Home Page | Jobs Dashboard | Recruiter Panel | AI Applicant Ranking |
|---|---|---|---|
| *(Add Screenshot)* | *(Add Screenshot)* | *(Add Screenshot)* | *(Add Screenshot)* |

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
