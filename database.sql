-- ============================================================
--  TalentAI — Database Schema
--  Run this script ONCE to create the database and tables.
--  After that, SQLAlchemy (db.create_all) manages the schema.
-- ============================================================

CREATE DATABASE IF NOT EXISTS job_portal
  CHARACTER SET utf8mb4
  COLLATE utf8mb4_unicode_ci;

USE job_portal;

-- ── users ──────────────────────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS users (
  id            INT UNSIGNED    NOT NULL AUTO_INCREMENT,
  full_name     VARCHAR(120)    NOT NULL,
  email         VARCHAR(150)    NOT NULL,
  password_hash VARCHAR(256)    NOT NULL,
  role          ENUM('seeker','recruiter') NOT NULL DEFAULT 'seeker',
  company_name  VARCHAR(150)    DEFAULT NULL,
  created_at    DATETIME        NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (id),
  UNIQUE KEY uq_users_email (email)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- ── jobs ───────────────────────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS jobs (
  id              INT UNSIGNED    NOT NULL AUTO_INCREMENT,
  title           VARCHAR(200)    NOT NULL,
  company         VARCHAR(150)    NOT NULL,
  location        VARCHAR(150)    NOT NULL,
  job_type        ENUM('Full-time','Part-time','Contract','Internship','Remote') NOT NULL DEFAULT 'Full-time',
  description     TEXT            NOT NULL,
  requirements    TEXT            NOT NULL,
  salary_range    VARCHAR(100)    DEFAULT NULL,
  skills_required TEXT            DEFAULT NULL,
  recruiter_id    INT UNSIGNED    NOT NULL,
  is_active       TINYINT(1)      NOT NULL DEFAULT 1,
  created_at      DATETIME        NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (id),
  KEY idx_jobs_recruiter (recruiter_id),
  KEY idx_jobs_active (is_active),
  CONSTRAINT fk_jobs_recruiter FOREIGN KEY (recruiter_id)
    REFERENCES users (id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- ── resumes ────────────────────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS resumes (
  id               INT UNSIGNED    NOT NULL AUTO_INCREMENT,
  user_id          INT UNSIGNED    NOT NULL,
  filename         VARCHAR(255)    NOT NULL,
  original_name    VARCHAR(255)    NOT NULL,
  extracted_text   LONGTEXT        DEFAULT NULL,
  extracted_skills TEXT            DEFAULT NULL,
  uploaded_at      DATETIME        NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (id),
  KEY idx_resumes_user (user_id),
  CONSTRAINT fk_resumes_user FOREIGN KEY (user_id)
    REFERENCES users (id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- ── applications ───────────────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS applications (
  id               INT UNSIGNED    NOT NULL AUTO_INCREMENT,
  job_id           INT UNSIGNED    NOT NULL,
  user_id          INT UNSIGNED    NOT NULL,
  resume_id        INT UNSIGNED    DEFAULT NULL,
  cover_letter     TEXT            DEFAULT NULL,
  similarity_score FLOAT           NOT NULL DEFAULT 0.0,
  status           ENUM('pending','reviewed','shortlisted','rejected') NOT NULL DEFAULT 'pending',
  applied_at       DATETIME        NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (id),
  UNIQUE KEY uq_job_user (job_id, user_id),
  KEY idx_applications_job  (job_id),
  KEY idx_applications_user (user_id),
  CONSTRAINT fk_applications_job FOREIGN KEY (job_id)
    REFERENCES jobs (id) ON DELETE CASCADE,
  CONSTRAINT fk_applications_user FOREIGN KEY (user_id)
    REFERENCES users (id) ON DELETE CASCADE,
  CONSTRAINT fk_applications_resume FOREIGN KEY (resume_id)
    REFERENCES resumes (id) ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
