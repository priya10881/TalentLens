
import json
from pathlib import Path

from pdf_reader import extract_text_from_pdf

from resume_analyzer import analyze_resume

from textract_parser import (
    clean_resume_text,
    extract_email,
    extract_skills,
    extract_skills_by_category,
    extract_skills_from_text,
    extract_skill_evidence,
    extract_resume_profile,
)

from skills_matcher import match_skills


# ============================================================
# PROJECT PATHS
# ============================================================

BASE_DIR = Path(__file__).parent

# Default sample resume
pdf_file = BASE_DIR / "sample_tech_resume.pdf"

# JSON output file
json_output_file = BASE_DIR / "resume_screening_result.json"


# ============================================================
# SUITABILITY SUMMARY
# ============================================================

def generate_suitability_summary(match_result):
    """
    Generate a rule-based suitability summary.

    This is not an AI-generated summary.
    """
    percentage = match_result["match_percentage"]
    matched = match_result["matched_skills"]
    missing = match_result["missing_skills"]

    if percentage >= 80:
        assessment = (
            "The candidate's detected skills strongly align "
            "with the job requirements."
        )
    elif percentage >= 50:
        assessment = (
            "The candidate's detected skills align with several "
            "of the job requirements, but some gaps remain."
        )
    elif percentage > 0:
        assessment = (
            "The candidate has some detected matching skills, "
            "but several job requirements are not matched."
        )
    else:
        assessment = (
            "No matching skills were detected using the current "
            "skill dictionary."
        )

    if matched:
        matched_text = "Matched skills: " + ", ".join(matched) + "."
    else:
        matched_text = "No matching skills were detected."

    if missing:
        missing_text = "Missing detected requirements: " + ", ".join(missing) + "."
    else:
        missing_text = "All recognized job requirements matched."

    return f"{assessment} {matched_text} {missing_text}"


# ============================================================
# SAVE STRUCTURED JSON
# ============================================================

def save_json_report(data, output_path):
    """Save the screening result as a JSON file."""
    output_path = Path(output_path)

    with output_path.open("w", encoding="utf-8") as file:
        json.dump(data, file, indent=4, ensure_ascii=False)


# ============================================================
# RESUME SCREENING
# ============================================================

def screen_resume(pdf_path, job_description, json_output_path=None):
    """Parse a PDF resume and compare it with a job description."""

    path = Path(pdf_path)

    # --------------------------------------------------------
    # Validate the resume file
    # --------------------------------------------------------

    if not path.exists():
        print(f"Error: Resume file not found: {path}")
        return None

    if not path.is_file():
        print("Error: The resume path is not a file.")
        return None

    if path.suffix.lower() != ".pdf":
        print("Error: Please provide a PDF resume.")
        return None

    # --------------------------------------------------------
    # Validate the job description
    # --------------------------------------------------------

    if not job_description or not job_description.strip():
        print("Error: Job description cannot be empty.")
        return None

    # --------------------------------------------------------
    # Extract text from the PDF
    # --------------------------------------------------------

    try:
        raw_text = extract_text_from_pdf(path)
    except (OSError, ValueError) as error:
        print(f"Error reading resume: {error}")
        return None

    if not raw_text or not raw_text.strip():
        print("Error: No readable text found in the PDF.")
        return None

    cleaned_text = clean_resume_text(raw_text)

    # --------------------------------------------------------
    # Extract candidate profile
    # --------------------------------------------------------

    profile = extract_resume_profile(cleaned_text)

    # --------------------------------------------------------
    # Extract skills and evidence
    # --------------------------------------------------------

    categorized_skills = extract_skills_by_category(cleaned_text)
    candidate_skills = extract_skills(cleaned_text)
    skill_evidence = extract_skill_evidence(cleaned_text)

    # --------------------------------------------------------
    # Extract job requirements
    # --------------------------------------------------------

    required_skills = extract_skills_from_text(job_description)

    if not required_skills:
        print("Error: No recognized skills found in the job description.")
        print(
            "Please include skills supported by the current "
            "skill dictionary."
        )
        return None

    # --------------------------------------------------------
    # Match candidate skills against job requirements
    # --------------------------------------------------------

    match_result = match_skills(
        required_skills,
        candidate_skills,
    )

    suitability_summary = generate_suitability_summary(match_result)

    # --------------------------------------------------------
    # Gemini AI analysis
    # --------------------------------------------------------

    ai_analysis = None

    try:
        ai_analysis = analyze_resume(
            cleaned_text,
            job_description,
        )

        suitability_summary = ai_analysis["suitability_summary"]
        summary_type = "gemini"

        print("\nGemini AI analysis completed successfully.")

    except Exception as error:
        ai_analysis = None
        summary_type = "rule-based-fallback"

        print(f"\nGemini analysis unavailable: {error}")
        print("Using the existing rule-based suitability summary.")

    # --------------------------------------------------------
    # Build structured JSON data
    # --------------------------------------------------------

    report = {
        "candidateName": profile["candidateName"],
        "email": profile["email"],
        "skills": candidate_skills,
        "skillsByCategory": categorized_skills,
        "skillEvidence": skill_evidence,
        "education": profile["education"],
        "workExperience": profile["workExperience"],
        "projects": profile["projects"],
        "jobDescription": job_description.strip(),
        "requiredSkills": required_skills,
        "matchingSkills": match_result["matched_skills"],
        "missingSkills": match_result["missing_skills"],
        "matchPercentage": match_result["match_percentage"],
        "suitabilitySummary": suitability_summary,
        "summaryType": summary_type,
        "aiAnalysis": ai_analysis,  
    }

    # --------------------------------------------------------
    # Display console report
    # --------------------------------------------------------

    print("\n========== RESUME SCREENING REPORT ==========")
    print(f"Resume File: {path.name}")
    print(f"Candidate Name: {profile['candidateName'] or 'Not found'}")
    print(f"Candidate Email: {profile['email'] or 'Not found'}")

    print("\n--- Skills by Category ---")

    for category, skills in categorized_skills.items():
        print(f"{category}: {skills or 'None detected'}")

    print("\n--- Skill Evidence ---")

    for source, categories in skill_evidence.items():
        print(f"\n{source}:")

        if not categories:
            print("  None detected")
            continue

        for category, skills in categories.items():
            print(f"  {category}: {skills}")

    print("\n--- Education ---")
    print(profile["education"] or "Not found")

    print("\n--- Work Experience ---")
    print(profile["workExperience"] or "Not found")

    print("\n--- Projects ---")
    print(profile["projects"] or "Not found")

    print("\n--- Job Match ---")
    print(f"Required Skills: {required_skills}")
    print(f"Candidate Skills: {candidate_skills}")
    print(f"Matched Skills: {match_result['matched_skills']}")
    print(f"Missing Skills: {match_result['missing_skills']}")
    displayed_percentage = (
    ai_analysis.get("match_percentage", match_result["match_percentage"])
    if ai_analysis is not None
    else match_result["match_percentage"]
    )

    print(f"Rule-Based Match Percentage: {match_result['match_percentage']}%")
    print(f"AI Match Percentage: {displayed_percentage}%")
    print(f"Summary Type: {summary_type}")

    print("\n--- Suitability Summary ---")
    print(suitability_summary)

    # --------------------------------------------------------
    # Optionally save JSON to a file
    # --------------------------------------------------------

    if json_output_path is not None:
        try:
            save_json_report(report, json_output_path)
            print(f"\nJSON report saved to: {Path(json_output_path).resolve()}")
        except OSError as error:
            print(f"\nError saving JSON report: {error}")

    print("==============================================")

    return report


# ============================================================
# MAIN PROGRAM
# ============================================================

if __name__ == "__main__":
    print("========== JOB DESCRIPTION INPUT ==========")
    print("Paste the job description below.")
    print("Type END on a new line when finished.\n")

    description_lines = []

    try:
        while True:
            line = input()

            if line.strip().upper() == "END":
                break

            description_lines.append(line)

    except (EOFError, KeyboardInterrupt):
        print("\nInput cancelled.")
        raise SystemExit(1)

    job_description = "\n".join(description_lines)

    screen_resume(
        pdf_file,
        job_description,
        json_output_path=json_output_file,
    )
