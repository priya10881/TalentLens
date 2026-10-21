# AI-Powered Resume Screening and Parsing

An AI-assisted resume screening project that combines resume parsing,
skill matching, candidate data storage, and GitHub profile retrieval.

## Features

- Parse resumes from PDF files.
- Extract candidate details and technical skills.
- Compare extracted skills with a job description.
- Generate an AI-assisted screening summary using Google Gemini.
- Store candidate records and screening results in Amazon DynamoDB.
- Store uploaded resume PDFs in Amazon S3.
- Retrieve GitHub profile and repository information using the GitHub API.

## Technology Stack

- Python
- Amazon S3
- Amazon DynamoDB
- AWS SDK for Python (boto3)
- Google Gemini API
- GitHub API
- PDF parsing

## Project Files

- `main.py` — Resume screening entry point.
- `pdf_reader.py` — PDF reading utilities.
- `resume_analyzer.py` — AI-assisted resume analysis.
- `skills_matcher.py` — Skill matching.
- `textract_parser.py` — Resume parsing utilities.
- `database.py` — DynamoDB operations.
- `process_uploaded_resume.py` — Downloads an uploaded resume from S3, screens it, and saves results to DynamoDB.
- `github_api.py` — GitHub API integration.
- `candidate_service.py` — Candidate retrieval and enrichment.
- `integrated_screening.py` — Screening integration workflow.
- `gemini_resume_analyzer.py` — Gemini-based analysis utilities.

## Setup

Use Python 3.11 or newer, subject to compatibility with the installed
versions of the project dependencies.

Create and activate a virtual environment:

```bash
python3 -m venv .venv
source .venv/bin/activate
cd ~/resume-screening-member-h

cat > README.md <<'EOF'
# AI-Powered Resume Screening and Parsing

An AI-assisted resume screening project combining PDF resume parsing,
skill matching, AI analysis, and candidate data storage.

## Features

- Extract candidate information and skills from PDF resumes.
- Match candidate skills against a job description.
- Generate AI-assisted screening summaries using Google Gemini.
- Store candidate records and screening results in Amazon DynamoDB.
- Store uploaded resumes in Amazon S3.
- Retrieve GitHub profile and repository information.

## Technology Stack

- Python
- Amazon S3
- Amazon DynamoDB
- Boto3
- Google Gemini API
- GitHub API

## Setup

Create a virtual environment:

    python3 -m venv .venv
    source .venv/bin/activate

Install the dependencies:

    pip install -r requirements.txt

Configure AWS credentials using a secure AWS credentials provider.
Configure the Gemini API key using an environment variable.
Never commit API keys or AWS credentials.

## Process an Uploaded Resume

After the candidate record and uploaded PDF are available, run:

    python process_uploaded_resume.py <candidate-id>

The script downloads the resume from S3, processes it, and updates
the corresponding candidate record in DynamoDB.

Resume processing currently runs through this Python script manually.
This repository does not automatically configure an S3 event trigger.

## Security

- Never commit `.env` files, API keys, or AWS credentials.
- Use appropriate IAM permissions.
- Do not publish real candidate resumes or personal information.
