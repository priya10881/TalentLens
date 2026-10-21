import re





# ============================================================

# SKILL DICTIONARY

# ============================================================



SKILL_CATEGORIES = {

    
    "Technical Skills": {
        "Python": ["Python"],
        "Java": ["Java"],
        "C": ["C programming", "C language", "programming in C"],
        "C++": ["C++"],
        "SQL": ["SQL", "Structured Query Language"],
        "MySQL": ["MySQL"],
        "Machine Learning": ["Machine Learning"],
        "Data Analysis": ["Data Analysis", "Data Analytics"],
        "Data Visualization": ["Data Visualization", "Data Visualisation"],
        "Pandas": ["Pandas"],
        "NumPy": ["NumPy", "Numpy"],
        "HTML": ["HTML"],
        "CSS": ["CSS"],
        "JavaScript": ["JavaScript"],
        "React": ["React"],
        "Node.js": ["Node.js"],
        "Docker": ["Docker"],
        "Linux": ["Linux"],
        "TensorFlow": ["TensorFlow"],
        "Spring Boot": ["Spring Boot"],
        "REST APIs": ["REST APIs", "REST API", "RESTful APIs", "RESTful API"],
        "Hibernate": ["Hibernate"],
        "Microservices": ["Microservices", "Microservice Architecture"],
        "Maven": ["Maven"],
        "Unit Testing": ["Unit Testing", "Unit Tests", "Unit Testing Frameworks"],
        "Kubernetes": ["Kubernetes", "K8s"],
        "Data Structures": ["Data Structures"],
        "Algorithms": ["Algorithms"],
        "GitHub": ["GitHub"],
    },


    
    "Cloud & DevOps": {
        "AWS": ["AWS", "Amazon Web Services"],
        "Azure": ["Azure", "Microsoft Azure"],
        "Git": ["Git"],
        "Kubernetes": ["Kubernetes", "K8s"],
    },



    "Tools & Software": {

        "Microsoft Office": ["Microsoft Office", "MS Office"],

        "Word": ["Microsoft Word", "MS Word"],

        "Excel": ["Microsoft Excel", "Excel"],

        "PowerPoint": ["Microsoft PowerPoint", "PowerPoint"],

        "OneNote": ["OneNote"],

        "Outlook": ["Outlook"],

        "Prezi": ["Prezi"],

        "Canva": ["Canva"],

        "Blackboard": ["Blackboard"],

        "Power BI": ["Power BI"],

    },



    "Soft Skills": {

        "Communication": [

            "Communication",

            "Communication skills",

            "Communicate",

            "Communicates",

            "Communicated",

            "Communicating",

            "Verbal communication",

            "Written communication",

        ],

        "Leadership": [

            "Leadership",

            "Leadership skills",

            "Leader",

            "Leaders",

            "Led a team",

            "Led",

            "Leading",

            "Managed a team",

            "Supervised a team",

        ],

        "Teamwork": [

            "Teamwork",

            "Team work",

            "Collaboration",

            "Collaborate",

            "Collaborates",

            "Collaborated",

            "Collaborating",

            "Collaborative",

            "Worked with a team",

            "Team player",

        ],

        "Problem-solving": [

            "Problem-solving",

            "Problem solving",

            "Solved problems",

            "Resolve problems",

            "Resolved problems",

            "Resolved issues",

            "Critical problem solving",

        ],

        "Critical thinking": [

            "Critical thinking",

            "Critical thinker",

            "Analytical thinking",

            "Analytical skills",

        ],

        "Teaching": [

            "Teaching",

            "Taught",

            "Teach",

            "Mentored",

            "Mentoring",

        ],

        "Customer service": [

            "Customer service",

            "Assisted customers",

            "Helped customers",

            "Resolved issues for customers",

        ],

        "Research": [

            "Research",

            "Researched",

            "Conducted research",

        ],

        "Time management": [

            "Time management",

            "Managed time effectively",

        ],

        "Organization": [

            "Organization",

            "Organizational skills",

            "Organized activities",

        ],

        "Training": [

            "Training",

            "Trained",

            "Train",

            "Trains",

        ],

    },



    "Languages": {

        "English": ["English"],

        "Spanish": ["Spanish"],

        "French": ["French"],

        "Hindi": ["Hindi"],

    },

}





# ============================================================

# RESUME SECTION HEADINGS

# ============================================================



SKILLS_HEADINGS = {

    "SKILLS",

    "TECHNICAL SKILLS",

    "CORE SKILLS",

    "KEY SKILLS",

    "SKILLS AND ABILITIES",

    "TECHNICAL AND PROFESSIONAL SKILLS",

    "CORE COMPETENCIES",

}



OTHER_SECTION_HEADINGS = {

    "EXPERIENCE",

    "WORK EXPERIENCE",

    "PROFESSIONAL EXPERIENCE",

    "EMPLOYMENT HISTORY",

    "PROJECTS",

    "ACADEMIC PROJECTS",

    "PERSONAL PROJECTS",

    "EDUCATION",

    "CERTIFICATIONS",

    "ACHIEVEMENTS",

    "LEADERSHIP",

    "VOLUNTEER EXPERIENCE",

    "ACTIVITIES",

    "INTERESTS",

    "LANGUAGES",

    "SUMMARY",

    "PROFILE",

    "OBJECTIVE",

    "PROFESSIONAL SUMMARY",

    "INTERNSHIPS",

    "PUBLICATIONS",
    "SOFT SKILLS",
    "TOOLS",
    "TOOLS AND TECHNOLOGIES",
    "TECHNOLOGIES",
    "AWARDS",
    "REFERENCES",
    "HOBBIES",
    "CAREER OBJECTIVE",
    "ABOUT ME",
    "PERSONAL DETAILS",
    "CONTACT",
    "CONTACT INFORMATION",

}





# ============================================================

# TEXT CLEANING

# ============================================================



def clean_resume_text(text):

    """Clean extracted resume text."""

    if not text:

        return ""



    text = text.replace("\r\n", "\n").replace("\r", "\n")

    text = re.sub(r"[ \t]+", " ", text)

    text = re.sub(r"\n[ \t]+", "\n", text)

    text = re.sub(r"\n{3,}", "\n\n", text)



    return text.strip()





# ============================================================

# EMAIL EXTRACTION

# ============================================================



def normalize_heading(line):
    """Normalize headings such as '## Education' to 'EDUCATION'."""
    line = line.strip()
    line = re.sub(r"^[#\s]+|[#\s]+$", "", line)
    return line.strip().upper()


def extract_email(text):

    """Extract the first email address found."""

    if not text:

        return None



    pattern = (

        r"\b[A-Za-z0-9._%+-]+"

        r"@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b"

    )



    match = re.search(pattern, text)

    return match.group(0) if match else None





# ============================================================

# SKILLS SECTION DETECTION

# ============================================================



def find_skills_section(text):
    """Find the dedicated skills section of a resume."""
    if not text:
        return None

    lines = clean_resume_text(text).splitlines()
    skill_headings = {normalize_heading(x) for x in SKILLS_HEADINGS}
    other_headings = {normalize_heading(x) for x in OTHER_SECTION_HEADINGS}

    for index, line in enumerate(lines):
        if normalize_heading(line) in skill_headings:
            section_lines = []
            for next_line in lines[index + 1:]:
                heading = normalize_heading(next_line)
                if heading in other_headings or heading in skill_headings:
                    break
                section_lines.append(next_line)
            return "\n".join(section_lines).strip()
    return None


def contains_skill(text, skill_name):

    """Check for a whole skill or phrase, ignoring capitalization."""

    if not text or not skill_name:

        return False



    pattern = (

        r"(?<!\w)"

        + re.escape(skill_name)

        + r"(?!\w)"

    )



    return re.search(pattern, text, re.IGNORECASE) is not None





def extract_skills_from_section(text):

    """Extract recognized skills from a block of text."""

    found_by_category = {}



    for category, skills in SKILL_CATEGORIES.items():

        found = []



        for canonical_name, aliases in skills.items():

            if any(

                contains_skill(text, alias)

                for alias in aliases

            ):

                found.append(canonical_name)



        found_by_category[category] = sorted(

            found,

            key=str.lower

        )



    return found_by_category





# ============================================================

# SKILLS BY CATEGORY

# ============================================================



def extract_skills_by_category(text):

    """

    Return detected skills by category.



    Explicitly listed skills and skills mentioned elsewhere

    are both included in the overall category results.

    """

    cleaned_text = clean_resume_text(text)



    all_resume_skills = extract_skills_from_section(cleaned_text)



    return {

        category: sorted(skills, key=str.lower)

        for category, skills in all_resume_skills.items()

    }





# ============================================================

# SKILL EVIDENCE

# ============================================================



def extract_skill_evidence(text):
    """Separate explicitly listed skills from skills detected elsewhere."""
    cleaned_text = clean_resume_text(text)
    evidence = {"Explicit Skills": {}, "Experience-Based Skills": {}}
    skill_headings = {normalize_heading(x) for x in SKILLS_HEADINGS}
    other_headings = {normalize_heading(x) for x in OTHER_SECTION_HEADINGS}
    current_source = "Experience-Based Skills"

    for line in cleaned_text.splitlines():
        heading = normalize_heading(line)
        if heading in skill_headings:
            current_source = "Explicit Skills"
            continue
        if heading in other_headings:
            current_source = "Experience-Based Skills"
            continue
        detected = extract_skills_from_section(line)
        for category, skills in detected.items():
            for skill in skills:
                evidence[current_source].setdefault(category, [])
                if skill not in evidence[current_source][category]:
                    evidence[current_source][category].append(skill)

    for source in evidence:
        for category in evidence[source]:
            evidence[source][category].sort(key=str.lower)
    return evidence


def extract_skills(text):

    """Return all detected resume skills as one list."""

    categorized = extract_skills_by_category(text)



    all_skills = []



    for skills in categorized.values():

        all_skills.extend(skills)



    return sorted(set(all_skills), key=str.lower)





# ============================================================

# JOB DESCRIPTION SKILL EXTRACTION

# ============================================================



def extract_skills_from_text(text):

    """Extract recognized skills from a job description."""

    if not text:

        return []



    categorized = extract_skills_from_section(text)



    found_skills = []



    for skills in categorized.values():

        found_skills.extend(skills)



    return sorted(set(found_skills), key=str.lower)





# ============================================================

# CANDIDATE PROFILE EXTRACTION

# ============================================================





RESUME_SECTION_ALIASES = {

    "education": {

        "EDUCATION",

        "ACADEMIC BACKGROUND",

        "EDUCATIONAL BACKGROUND",

    },

    "experience": {

        "EXPERIENCE",

        "WORK EXPERIENCE",

        "PROFESSIONAL EXPERIENCE",

        "EMPLOYMENT HISTORY",

        "INTERNSHIPS",

        "EDUCATION-RELATED EXPERIENCE",

        "RESEARCH EXPERIENCE",

        "ADDITIONAL WORK EXPERIENCE",

    },

    "projects": {

        "PROJECTS",

        "ACADEMIC PROJECTS",

        "PERSONAL PROJECTS",

        "PROJECT EXPERIENCE",

    },

}







def extract_resume_sections(text):
    """Extract education, experience, and projects using section headings."""
    cleaned_text = clean_resume_text(text)
    sections = {"education": "", "experience": "", "projects": ""}
    current_section = None

    normalized_aliases = {
        section: {normalize_heading(alias) for alias in aliases}
        for section, aliases in RESUME_SECTION_ALIASES.items()
    }
    all_headings = {normalize_heading(x) for x in SKILLS_HEADINGS}
    all_headings.update(normalize_heading(x) for x in OTHER_SECTION_HEADINGS)
    for aliases in normalized_aliases.values():
        all_headings.update(aliases)

    for line in cleaned_text.splitlines():
        heading = normalize_heading(line)
        matched_section = None
        for section_name, aliases in normalized_aliases.items():
            if heading in aliases:
                matched_section = section_name
                break
        if matched_section:
            current_section = matched_section
            continue
        if heading in all_headings:
            current_section = None
            continue
        if current_section:
            if sections[current_section]:
                sections[current_section] += "\n"
            sections[current_section] += line.strip()

    return {key: value.strip() for key, value in sections.items()}


def extract_candidate_name(text):
    """Return the first suitable name-like line, removing Markdown markers."""
    if not text:
        return None

    skill_headings = {normalize_heading(x) for x in SKILLS_HEADINGS}
    other_headings = {normalize_heading(x) for x in OTHER_SECTION_HEADINGS}
    non_name_headings = {
        "SOFTWARE ENGINEER", "DATA SCIENTIST", "DATA ANALYST",
        "WEB DEVELOPER", "FULL STACK DEVELOPER", "FRONTEND DEVELOPER",
        "BACKEND DEVELOPER", "PYTHON DEVELOPER", "PROJECT MANAGER",
        "SYSTEMS ENGINEER", "STUDENT", "RESUME", "CURRICULUM VITAE",
        "CURRICULUM VITAE (CV)",
    }

    for line in clean_resume_text(text).splitlines():
        candidate = line.strip()
        candidate = re.sub(r"^[#*\-\s]+", "", candidate)
        candidate = re.sub(r"[*#\s]+$", "", candidate).strip()
        if not candidate:
            continue
        if extract_email(candidate):
            continue
        if re.search(r"https?://|www\.|@", candidate, re.IGNORECASE):
            continue
        if re.search(r"\d{3,}", candidate):
            continue
        normalized = normalize_heading(candidate)
        if normalized in skill_headings or normalized in other_headings:
            continue
        if normalized in non_name_headings:
            continue
        if len(candidate) > 70 or len(candidate.split()) > 5:
            continue
        return candidate
    return None


def extract_resume_profile(text):

    """

    Return a structured profile using rule-based extraction.

    """

    sections = extract_resume_sections(text)



    return {

        "candidateName": extract_candidate_name(text),

        "email": extract_email(text),

        "skills": extract_skills(text),

        "education": sections["education"] or None,

        "workExperience": sections["experience"] or None,

        "projects": sections["projects"] or None,

    }







# ============================================================

# DIRECT TESTING

# ============================================================



if __name__ == "__main__":

    sample_resume = """

    Alex Morgan



    EXPERIENCE

    Led a team of volunteers.

    Collaborated with colleagues.

    Conducted research on student learning.

    Trained new team members.

    Resolved issues for customers.

    Used Python for data analysis.



    ## SKILLS

    Python, SQL, Excel, Canva

    Spanish, English



    ## EDUCATION

    Bachelor of Science

    """



    cleaned = clean_resume_text(sample_resume)



    print("Email:", extract_email(cleaned))

    print("\nSkills section:")

    print(find_skills_section(cleaned))



    print("\nSkills by category:")

    for category, skills in extract_skills_by_category(cleaned).items():

        print(f"{category}: {skills or 'None detected'}")



    print("\nSkill evidence:")

    for source, categories in extract_skill_evidence(cleaned).items():

        print(f"\n{source}:")



        if not categories:

            print("  None detected")

            continue



        for category, skills in categories.items():

            print(f"  {category}: {skills}")



    job_description = """

    We need Python, SQL, AWS, Git,

    Excel, communication, leadership, and teamwork.

    """



    print("\nJob description skills:")

    print(extract_skills_from_text(job_description))
