def get_answer_from_resume(question: str, resume_data: dict):
    q = question.lower()

    # Basic keyword matching logic
    if "name" in q:
        return resume_data.get("name")
    elif "email" in q:
        return resume_data.get("email")
    elif "phone" in q or "mobile" in q:
        return resume_data.get("phone")
    elif "experience" in q or "years" in q:
        return resume_data.get("experience")
    elif "skill" in q or "technology" in q or "tech stack" in q:
        return resume_data.get("skills")
    elif "location" in q or "city" in q:
        return resume_data.get("location")
    elif "notice" in q:
        return resume_data.get("notice_period")
    elif "current" in q and "company" in q:
        return "Honeywell"  # Optional
    elif "expected" in q and "salary" in q:
        return "As per company standards"
    elif "relocate" in q or "relocation" in q:
        return "Yes"
    elif "willing" in q and "shift" in q:
        return "Yes"
    elif "python" in q:
        return "Yes, I have hands-on experience with Python automation."
    else:
        return None
