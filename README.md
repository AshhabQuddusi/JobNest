# JobNest — AI-Powered Job Portal with Resume Ranking System

> A full-stack Flask web application that uses \\\*\\\*TF-IDF + cosine similarity\\\*\\\* to automatically rank job applicants based on how well their resume matches a job description.

\---

## 📸 Screenshots

|Landing Page|Job Listings|Recruiter Dashboard|AI Ranking View|
|:-:|:-:|:-:|:-:|
|*(screenshot)*|*(screenshot)*|*(screenshot)*|*(screenshot)*|

\---

## ✨ Features

### For Job Seekers

* Register / login as a **Job Seeker**
* Upload **PDF resumes** — skills extracted automatically via `pdfplumber`
* Browse, search, and filter all active job postings
* Apply to jobs with a selected resume + optional cover letter
* View all applications and their AI match score on a personal dashboard
* Withdraw applications at any time

### For Recruiters

* Register / login as a **Recruiter**
* Post, edit, and delete job openings
* View all applicants for each job, **ranked by AI similarity score**
* Download candidate resumes
* Update application statuses: Pending → Reviewed → Shortlisted / Rejected

### AI Ranking Engine

* Extracts full text from candidate PDFs
* Combines job title, description, requirements, and skills into a single corpus
* Vectorises documents using **TF-IDF** (scikit-learn, bigrams, sublinear TF)
* Computes **cosine similarity** between the job vector and each resume vector
* Displays ranked candidates with a visual match percentage bar

\---

## 🛠 Tech Stack

|Layer|Technology|
|-|-|
|Backend|Python 3.10+, Flask 3|
|ORM|Flask-SQLAlchemy (SQLAlchemy 2)|
|Database|MySQL 8|
|Auth|Flask-Login + Werkzeug password hashing|
|Resume Parsing|pdfplumber|
|NLP / Ranking|scikit-learn (TfidfVectorizer + cosine\_similarity)|
|Frontend|Vanilla HTML5, CSS3, JavaScript (no frameworks)|
|Fonts|Google Fonts — Syne + DM Sans|

\---

## 📁 Project Structure

```
project\\\_root/
├── app.py                  # Application factory \\\& entry point
├── config.py               # Configuration (reads .env)
├── extensions.py           # Flask extensions (db, login\\\_manager)
├── requirements.txt
├── database.sql            # Raw SQL schema
├── .env.example
├── README.md
│
├── models/
│   ├── \\\_\\\_init\\\_\\\_.py
│   ├── user.py
│   ├── job.py
│   ├── resume.py
│   └── application.py
│
├── routes/
│   ├── \\\_\\\_init\\\_\\\_.py
│   ├── auth.py             # /register, /login, /logout
│   ├── main.py             # / (landing)
│   ├── jobs.py             # /jobs, /jobs/<id>
│   ├── recruiter.py        # /recruiter/\\\* (dashboard, post job, applicants)
│   └── seeker.py           # /seeker/\\\* (dashboard, upload, apply)
│
├── utils/
│   ├── \\\_\\\_init\\\_\\\_.py
│   ├── resume\\\_parser.py    # PDF → text + skill extraction
│   ├── ranking.py          # TF-IDF cosine similarity ranking
│   └── helpers.py          # File upload helpers
│
├── templates/
│   ├── base.html
│   ├── index.html
│   ├── login.html
│   ├── register.html
│   ├── jobs/
│   │   ├── list.html
│   │   └── detail.html
│   ├── recruiter/
│   │   ├── dashboard.html
│   │   ├── post\\\_job.html
│   │   └── applicants.html
│   ├── seeker/
│   │   ├── dashboard.html
│   │   ├── upload\\\_resume.html
│   │   └── apply.html
│   └── errors/
│       ├── 403.html
│       ├── 404.html
│       └── 500.html
│
├── static/
│   ├── css/style.css
│   └── js/main.js
│
└── uploads/                # Created automatically at runtime
```

\---

## ⚙️ Setup Instructions

### Prerequisites

* Python 3.10 or higher
* MySQL 8.0 or higher
* pip

### 1\. Clone the repository

```bash
git clone https://github.com/yourname/JobNest.git
cd talentai/project\\\_root
```

### 2\. Create and activate a virtual environment

```bash
python -m venv venv

# Linux / macOS
source venv/bin/activate

# Windows
venv\\\\Scripts\\\\activate
```

### 3\. Install dependencies

```bash
pip install -r requirements.txt
```

### 4\. Configure environment variables

```bash
cp .env.example .env
```

Edit `.env` and fill in your MySQL credentials:

```
SECRET\\\_KEY=change-this-to-a-random-secret
DB\\\_HOST=localhost
DB\\\_PORT=3306
DB\\\_USER=root
DB\\\_PASSWORD=your\\\_mysql\\\_password
DB\\\_NAME=job\\\_portal
```

### 5\. Set up the database

#### Option A — using the SQL script (recommended first run)

```bash
mysql -u root -p < database.sql
```

#### Option B — let SQLAlchemy create tables automatically

The application calls `db.create\\\_all()` on startup, so if your MySQL user has CREATE TABLE privileges, the tables will be created automatically when you run the app.

> The `database.sql` script also creates the `job\\\_portal` database. If you use Option B, create the database first:
> ```sql
> CREATE DATABASE job\\\_portal CHARACTER SET utf8mb4 COLLATE utf8mb4\\\_unicode\\\_ci;
> ```

### 6\. Run the application

```bash
python app.py
```

Visit **http://localhost:5000** in your browser.

\---

## 🗄️ Database Schema

### `users`

|Column|Type|Notes|
|-|-|-|
|id|INT PK|Auto-increment|
|full\_name|VARCHAR(120)||
|email|VARCHAR(150)|Unique, indexed|
|password\_hash|VARCHAR(256)|Werkzeug PBKDF2|
|role|ENUM|`seeker` or `recruiter`|
|company\_name|VARCHAR(150)|Recruiters only|
|created\_at|DATETIME||

### `jobs`

|Column|Type|Notes|
|-|-|-|
|id|INT PK||
|title|VARCHAR(200)||
|company|VARCHAR(150)||
|location|VARCHAR(150)||
|job\_type|ENUM|Full-time, Part-time, etc.|
|description|TEXT||
|requirements|TEXT||
|salary\_range|VARCHAR(100)|Optional|
|skills\_required|TEXT|Comma-separated|
|recruiter\_id|INT FK → users|CASCADE delete|
|is\_active|TINYINT||

### `resumes`

|Column|Type|Notes|
|-|-|-|
|id|INT PK||
|user\_id|INT FK → users||
|filename|VARCHAR(255)|UUID-prefixed stored name|
|original\_name|VARCHAR(255)|Original filename|
|extracted\_text|LONGTEXT|Full PDF text|
|extracted\_skills|TEXT|Comma-separated|
|uploaded\_at|DATETIME||

### `applications`

|Column|Type|Notes|
|-|-|-|
|id|INT PK||
|job\_id|INT FK → jobs||
|user\_id|INT FK → users||
|resume\_id|INT FK → resumes|SET NULL on delete|
|cover\_letter|TEXT|Optional|
|similarity\_score|FLOAT|0.0–1.0, computed by AI|
|status|ENUM|pending/reviewed/shortlisted/rejected|
|applied\_at|DATETIME||

Unique constraint: `(job\\\_id, user\\\_id)` — one application per seeker per job.

\---

## 🧠 How the Ranking Works

1. When a recruiter opens the **Applicants** view for a job, the ranking engine runs.
2. A **job corpus text** is built by concatenating: title + company + description + requirements + skills.
3. All resumes linked to that job's applications are loaded from the DB.
4. A `TfidfVectorizer` (bigrams, English stop-words, sublinear TF) is fitted on `\\\[job\\\_text] + \\\[resume\\\_texts]`.
5. **Cosine similarity** is computed between the job vector and each resume vector.
6. Scores (0.0 – 1.0) are written back to `applications.similarity\\\_score`.
7. Applicants are displayed in descending score order with a colour-coded match bar.

\---

## 🔒 Security Notes

* Passwords are hashed with **PBKDF2-SHA256** via Werkzeug.
* File uploads are sanitised with `werkzeug.utils.secure\\\_filename` and prefixed with a UUID.
* Role-based access control enforced on every protected route.
* SQL injection prevented by SQLAlchemy's parameterised queries.
* For production: set `DEBUG=False`, use HTTPS, and configure a proper `SECRET\\\_KEY`.

\---

## 📄 License

MIT — free to use for academic or personal projects.

