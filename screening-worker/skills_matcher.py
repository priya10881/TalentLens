
def match_skills(required_skills, candidate_skills):
    """Compare required skills with skills extracted from a resume."""

    def normalize(skill):
        return " ".join(skill.strip().lower().split())

    required_map = {
        normalize(skill): skill.strip()
        for skill in required_skills
        if skill and skill.strip()
    }

    candidate_map = {
        normalize(skill): skill.strip()
        for skill in candidate_skills
        if skill and skill.strip()
    }

    if not required_map:
        return {
            "match_percentage": 0,
            "matched_skills": [],
            "missing_skills": []
        }

    # Only treat genuinely equivalent names as aliases.
    # Related technologies are not automatically interchangeable.
    aliases = {
        "rest api": "rest apis",
        "restful api": "rest apis",
        "restful apis": "rest apis",
        "unit tests": "unit testing",
        "k8s": "kubernetes",
    }

    def canonical(skill):
        normalized = normalize(skill)
        return aliases.get(normalized, normalized)

    candidate_canonical = {
        canonical(skill)
        for skill in candidate_map
    }

    matched = []
    missing = []

    for normalized, original in required_map.items():
        if canonical(normalized) in candidate_canonical:
            matched.append(original)
        else:
            missing.append(original)

    score = round(len(matched) / len(required_map) * 100, 2)

    return {
        "match_percentage": score,
        "matched_skills": sorted(matched, key=str.lower),
        "missing_skills": sorted(missing, key=str.lower)
    }
