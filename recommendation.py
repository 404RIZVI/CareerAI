from collections import defaultdict

WEIGHTS = {
    "academics": 0.20,
    "interests": 0.25,
    "skills": 0.20,
    "preferences": 0.20,
    "aptitude": 0.15,
}

INTEREST_MAP = {
    "Artificial Intelligence": ["AI/ML Engineer", "Data Scientist", "Robotics Engineer"],
    "Programming": ["AI/ML Engineer", "Software Developer", "Data Scientist", "Cloud Engineer", "DevOps Engineer"],
    "Data": ["Data Scientist", "Data Analyst", "AI/ML Engineer", "Business Analyst"],
    "Finance": ["Financial Analyst", "Business Analyst", "Data Analyst"],
    "Business": ["Business Analyst", "Product Manager", "Financial Analyst"],
    "Cyber Security": ["Cyber Security Analyst", "Cloud Engineer", "DevOps Engineer"],
    "Design": ["UI/UX Designer", "Product Manager"],
    "Robotics": ["Robotics Engineer", "AI/ML Engineer"],
    "Cloud Computing": ["Cloud Engineer", "DevOps Engineer", "Software Developer"],
    "Research": ["AI/ML Engineer", "Data Scientist", "Robotics Engineer"],
    "Marketing": ["Product Manager", "Business Analyst", "UI/UX Designer"],
    "Management": ["Product Manager", "Business Analyst"],
}

SKILL_MAP = {
    "Python": ["AI/ML Engineer", "Data Scientist", "Data Analyst", "Software Developer", "Robotics Engineer"],
    "C/C++": ["Software Developer", "Robotics Engineer"],
    "JavaScript": ["Software Developer", "UI/UX Designer"],
    "HTML/CSS": ["Software Developer", "UI/UX Designer"],
    "SQL": ["Data Scientist", "Data Analyst", "Business Analyst", "Software Developer", "Financial Analyst"],
    "Excel": ["Data Analyst", "Financial Analyst", "Business Analyst", "Product Manager"],
    "Data Analysis": ["Data Scientist", "Data Analyst", "Business Analyst", "Financial Analyst"],
    "Mathematics": ["AI/ML Engineer", "Data Scientist", "Financial Analyst", "Robotics Engineer"],
    "Communication": ["Business Analyst", "Product Manager", "UI/UX Designer", "Financial Analyst"],
    "Design": ["UI/UX Designer", "Product Manager"],
    "Problem Solving": ["AI/ML Engineer", "Software Developer", "Cyber Security Analyst", "Data Scientist", "Robotics Engineer", "DevOps Engineer"],
    "Leadership": ["Product Manager", "Business Analyst"],
}

SUBJECT_MAP = {
    "Mathematics": ["AI/ML Engineer", "Data Scientist", "Data Analyst", "Financial Analyst", "Robotics Engineer"],
    "Physics": ["Robotics Engineer", "AI/ML Engineer", "Software Developer"],
    "Chemistry": ["AI/ML Engineer", "Robotics Engineer"],
    "Computer Science": ["AI/ML Engineer", "Software Developer", "Cyber Security Analyst", "Cloud Engineer", "DevOps Engineer"],
    "Accountancy": ["Financial Analyst", "Business Analyst", "Data Analyst"],
    "Economics": ["Financial Analyst", "Business Analyst", "Data Analyst"],
    "Business Studies": ["Business Analyst", "Product Manager", "Financial Analyst"],
    "English": ["UI/UX Designer", "Product Manager", "Business Analyst"],
    "History": ["Business Analyst", "Product Manager"],
    "Political Science": ["Business Analyst", "Product Manager"],
    "Psychology": ["UI/UX Designer", "Product Manager", "Business Analyst"],
}

APTITUDE_MAP = {
    0: ["Data Scientist", "Data Analyst", "AI/ML Engineer"],
    1: ["Software Developer", "AI/ML Engineer", "Cloud Engineer", "DevOps Engineer"],
    2: ["UI/UX Designer", "Product Manager"],
    3: ["Cyber Security Analyst", "AI/ML Engineer", "Robotics Engineer"],
    4: ["Business Analyst", "Product Manager", "Financial Analyst"],
}


def clamp(value, low=0, high=100):
    return max(low, min(high, value))


def normalize_selected_skills(skills):
    return {item.split("|")[0] if "|" in item else item for item in skills}


def academic_score(career, answers):
    subjects = answers.get("subjects", {})
    if not subjects:
        return 50.0
    relevant = 0
    total = 0
    for subject, mark in subjects.items():
        mark = float(mark)
        if career["name"] in SUBJECT_MAP.get(subject, []):
            relevant += mark
        total += mark
    return clamp(relevant / total * 100 if total else 50)


def interest_score(career, interests):
    if not interests:
        return 40.0
    hits = sum(career["name"] in INTEREST_MAP.get(i, []) for i in interests)
    return clamp(35 + (hits / max(1, len(interests))) * 65)


def skill_score(career, skills):
    selected = normalize_selected_skills(skills)
    required = set(career["skills"])
    if not required:
        return 50.0
    overlap = len(selected & required) / len(required)
    return clamp(30 + overlap * 70)


def preference_score(career, preferences):
    name = career["name"]
    p = {k: int(v) for k, v in preferences.items() if str(v).isdigit()}
    rules = {
        "AI/ML Engineer": {"coding": 5, "math": 5, "data": 4, "technical": 5, "research": 4, "physical": 2, "creative": 2, "business": 1},
        "Data Scientist": {"coding": 4, "math": 5, "data": 5, "technical": 4, "research": 5, "physical": 1, "creative": 2, "business": 2},
        "Software Developer": {"coding": 5, "math": 3, "data": 2, "technical": 5, "research": 2, "physical": 1, "creative": 3, "business": 1},
        "Data Analyst": {"coding": 3, "math": 4, "data": 5, "technical": 3, "research": 3, "physical": 1, "creative": 2, "business": 3},
        "Cyber Security Analyst": {"coding": 4, "math": 3, "data": 3, "technical": 5, "research": 5, "physical": 1, "creative": 1, "business": 1},
        "Financial Analyst": {"coding": 2, "math": 5, "data": 5, "technical": 2, "research": 3, "physical": 1, "creative": 1, "business": 5},
        "Cloud Engineer": {"coding": 4, "math": 2, "data": 2, "technical": 5, "research": 3, "physical": 1, "creative": 1, "business": 2},
        "UI/UX Designer": {"coding": 2, "math": 1, "data": 2, "technical": 2, "research": 3, "physical": 1, "creative": 5, "business": 3},
        "Business Analyst": {"coding": 1, "math": 3, "data": 4, "technical": 2, "research": 3, "physical": 1, "creative": 2, "business": 5},
        "Robotics Engineer": {"coding": 4, "math": 5, "data": 2, "technical": 5, "research": 5, "physical": 5, "creative": 3, "business": 1},
        "DevOps Engineer": {"coding": 4, "math": 2, "data": 2, "technical": 5, "research": 3, "physical": 1, "creative": 1, "business": 2},
        "Product Manager": {"coding": 2, "math": 2, "data": 3, "technical": 3, "research": 3, "physical": 1, "creative": 4, "business": 5},
    }
    target = rules.get(name, {})
    if not target:
        return 50.0
    keys = [k for k in target if k in p]
    if not keys:
        return 50.0
    closeness = sum(1 - abs(p[k] - target[k]) / 4 for k in keys) / len(keys)
    return clamp(40 + closeness * 60)


def aptitude_score(career, aptitude):
    if not aptitude:
        return 50.0
    hits = 0
    for idx, answer in enumerate(aptitude):
        try:
            option = int(answer)
        except (TypeError, ValueError):
            continue
        if career["name"] in APTITUDE_MAP.get(option, []):
            hits += 1
    return clamp(35 + hits / max(1, len(aptitude)) * 65)


def score_career(career, answers):
    parts = {
        "academics": academic_score(career, answers),
        "interests": interest_score(career, answers.get("interests", [])),
        "skills": skill_score(career, answers.get("skills", [])),
        "preferences": preference_score(career, answers.get("preferences", {})),
        "aptitude": aptitude_score(career, answers.get("aptitude", [])),
    }
    raw = sum(parts[k] * WEIGHTS[k] for k in WEIGHTS)
    return round(clamp(raw), 1), parts


def reasons_for(career, answers, parts):
    reasons = []
    interests = answers.get("interests", [])
    selected_skills = normalize_selected_skills(answers.get("skills", []))
    subjects = answers.get("subjects", {})

    matching_interests = [i for i in interests if career["name"] in INTEREST_MAP.get(i, [])]
    if matching_interests:
        reasons.append("Strong interest in " + ", ".join(matching_interests[:2]))
    matching_skills = list(selected_skills & set(career["skills"]))
    if matching_skills:
        reasons.append("Existing skills include " + ", ".join(matching_skills[:3]))
    strong_subjects = [s for s, m in subjects.items() if float(m) >= 75 and career["name"] in SUBJECT_MAP.get(s, [])]
    if strong_subjects:
        reasons.append("Good academic performance in " + ", ".join(strong_subjects[:2]))
    if parts["preferences"] >= 75:
        reasons.append("Your work preferences align well with this career")
    if parts["aptitude"] >= 70:
        reasons.append("Your assessment answers show a compatible problem-solving style")
    if not reasons:
        reasons.append("Your overall profile shows a balanced match with this career")
    return reasons[:5]


def recommend(careers, answers):
    scored = []
    for career in careers:
        score, parts = score_career(career, answers)
        scored.append({
            "career": career,
            "score": score,
            "parts": {k: round(v, 1) for k, v in parts.items()},
            "reasons": reasons_for(career, answers, parts)
        })
    scored.sort(key=lambda x: (-x["score"], x["career"]["name"]))
    return scored[:3], scored


def skill_gap(career, selected_skills):
    selected = normalize_selected_skills(selected_skills)
    required = career["skills"]
    have = [s for s in required if s in selected]
    missing = [s for s in required if s not in selected]
    pct = round(len(have) / max(1, len(required)) * 100)
    return {"current": have, "missing": missing, "percentage": pct}


def compare_careers(c1, c2, answers):
    a_score, a_parts = score_career(c1, answers)
    b_score, b_parts = score_career(c2, answers)
    return {
        "left": {"career": c1, "score": a_score, "parts": a_parts, "gap": skill_gap(c1, answers.get("skills", []))},
        "right": {"career": c2, "score": b_score, "parts": b_parts, "gap": skill_gap(c2, answers.get("skills", []))}
    }
