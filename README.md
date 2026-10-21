# AI-Powered Resume Screening and Parsing

An AI-assisted resume screening system that parses PDF resumes,
matches candidate skills against job descriptions, generates AI-assisted
screening summaries, and stores results in AWS.

## Features

- Extract candidate information and skills from PDF resumes.
- Match candidate skills against a job description.
- Generate AI-assisted screening summaries using Google Gemini.
- Store candidate records and screening results in Amazon DynamoDB.
- Store uploaded resume PDFs in Amazon S3.
- Generate presigned URLs for resume uploads through an API.
- Retrieve GitHub profile and repository information using the GitHub API.

## Technology Stack

- Python
- Amazon API Gateway
- AWS Lambda
- Amazon S3
- Amazon DynamoDB
- Boto3
- Google Gemini API
- GitHub REST API
- PDF parsing

## Project Files

| File | Purpose |
|---|---|
| `main.py` | Resume screening entry point |
| `pdf_reader.py` | PDF reading utilities |
| `resume_analyzer.py` | Resume analysis |
| `skills_matcher.py` | Skill matching |
| `textract_parser.py` | Resume parsing utilities |
| `database.py` | DynamoDB operations |
| `process_uploaded_resume.py` | Downloads, processes, and screens an uploaded resume |
| `github_api.py` | GitHub API integration |
| `candidate_service.py` | Candidate retrieval and GitHub profile enrichment |
| `integrated_screening.py` | Screening integration workflow |
| `gemini_resume_analyzer.py` | Gemini-based analysis utilities |

## Setup

Create and activate a virtual environment:

    python3 -m venv .venv
    source .venv/bin/activate

Install dependencies:

    pip install -r requirements.txt

Configure AWS credentials using a secure AWS credentials provider.
Configure your Gemini API key using the environment variable expected
by the application.

Never commit API keys, AWS credentials, or `.env` files.

## Resume Screening Workflow

1. Submit a candidate registration request to the API.
2. Receive a candidate ID and a presigned S3 upload URL.
3. Upload the resume PDF to Amazon S3.
4. Run the Python screening script with the candidate ID.
5. Extract resume information and analyze skills.
6. Generate an AI-assisted suitability summary.
7. Save screening results and the final status in DynamoDB.

Run screening for an uploaded candidate:

    python process_uploaded_resume.py <candidate-id>

Replace `<candidate-id>` with the actual candidate ID returned by the API.

**Current limitation:** Resume processing is initiated manually using the
Python script. Automatic screening triggered by an S3 upload has not
been implemented or verified.

## Security

- Never commit `.env` files, API keys, or AWS credentials.
- Apply least-privilege IAM permissions.
- Keep S3 objects private and protect presigned URLs.
- Use fictional or authorized sample resumes during demonstrations.
- Avoid publishing candidate personal information in logs or screenshots.
