import requests
import json
import re
from datetime import datetime
from utils.logger import get_logger

logger = get_logger(__name__)

HF_API_URL = "https://api-inference.huggingface.co/models/microsoft/phi-2"
HF_HEADERS = {"Authorization": "Bearer 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"}

def get_answer_from_resume(question, resume_data, hidden_json=None):
    def normalize(text):
        return re.sub(r'[^a-z0-9 ]', '', text.lower())

    def find_direct_match(question, data):
        q_words = set(normalize(question).split())
        flat = {}

        def flatten(obj, prefix=''):
            if isinstance(obj, dict):
                for k, v in obj.items():
                    flatten(v, prefix + k + " ")
            elif isinstance(obj, list):
                for i in obj:
                    flatten(i, prefix)
            else:
                flat[prefix.strip()] = str(obj)

        flatten(data)

        for key, value in flat.items():
            key_words = set(normalize(key).split())
            if key_words & q_words:
                return key.strip(), value.strip()
        return None, None

    # Direct match from JSON
    key, value = find_direct_match(question, hidden_json or {})
    if key and value:
        key_lower = key.lower()
        if "date" in key_lower or "dob" in key_lower or "birth" in key_lower:
            return f"My date of birth is {value}."
        elif "expected salary" in key_lower or "expected ctc" in key_lower:
            return f"My expected salary is {value}."
        elif "current salary" in key_lower or "current ctc" in key_lower:
            return f"My current salary is {value}."
        elif "location" in key_lower:
            return f"I am currently based in {value} and open to relocation."
        elif "experience" in key_lower:
            return f"I have {value} of professional experience."
        elif "pan" in key_lower:
            return f"My PAN number is {value}."
        elif "aadhar" in key_lower or "aadhaar" in key_lower:
            return f"My Aadhar number is {value}."
        elif value.lower() in ["yes", "no"]:
            return f"{value.capitalize()}, I am {key.lower()}."
        else:
            return f"{key}: {value}"

    # Experience fallback
    experience_match = re.search(
        r'(?:experience in|do you have experience in|how many years of experience in)\s+([a-zA-Z0-9\s\-]+)',
        question,
        re.IGNORECASE
    )
    if experience_match:
        skill = experience_match.group(1).strip().rstrip("?")
        return f"I have 2 years of experience in {skill}."

    # Date of Birth fallback
    dob_raw = hidden_json.get("Additional Details", {}).get("Date Of Birth", "11 January 1999")
    try:
        dob_dt = datetime.strptime(dob_raw, "%d %B %Y")
    except ValueError:
        dob_dt = None

    if re.search(r'\b(date of birth|dob|birthdate)\b', question, re.IGNORECASE):
        if "(dd/mm/yyyy)" in question.lower():
            return dob_dt.strftime("%d/%m/%Y") if dob_dt else "11/01/1999"
        elif "(dd-mm-yyyy)" in question.lower():
            return dob_dt.strftime("%d-%m-%Y") if dob_dt else "11-01-1999"
        else:
            return dob_dt.strftime("%d-%m-%Y") if dob_dt else dob_raw

    # PAN fallback
    if "pan" in question.lower():
        pan = hidden_json.get("Additional Details", {}).get("PAN Card No")
        if pan:
            return pan

    # Aadhar fallback
    if "aadhar" in question.lower() or "aadhaar" in question.lower():
        aadhar = hidden_json.get("Additional Details", {}).get("Aadhar Card No")
        if aadhar:
            return re.sub(r'(\d{4})(\d{4})(\d{4})', r'\1 \2 \3', aadhar.replace(" ", ""))

    # Phone fallback
    if "phone" in question.lower() or "mobile" in question.lower():
        phone = hidden_json.get("Contact Information", {}).get("Phone")
        if phone:
            return phone

    # Notice Period fallback
    if "notice period" in question.lower():
        notice = hidden_json.get("Additional Details", {}).get("Notice Period")
        if notice:
            return f"My notice period is {notice}."

    # Salary fallback
    if "expected salary" in question.lower():
        salary = hidden_json.get("Additional Details", {}).get("Expected Salary")
        if salary:
            return f"My expected salary is {salary}."
    if "current salary" in question.lower():
        salary = hidden_json.get("Additional Details", {}).get("Current Salary")
        if salary:
            return f"My current salary is {salary}."

    # Hugging Face fallback
    context = (
        f"Candidate Resume:\n{resume_data}\n\n"
        f"Additional Information:\n{json.dumps(hidden_json or {}, indent=2)}\n\n"
        f"Recruiter Question:\n{question}\n\n"
        f"Please respond briefly, positively, and professionally based on the candidate's background:"
    )

    payload = {
        "inputs": context,
        "parameters": {
            "max_new_tokens": 120,
            "temperature": 0.6,
            "return_full_text": False
        }
    }

    try:
        response = requests.post(HF_API_URL, headers=HF_HEADERS, json=payload)
        response.raise_for_status()
        data = response.json()

        if isinstance(data, list) and "generated_text" in data[0]:
            return data[0]["generated_text"].strip()
        elif isinstance(data, dict) and "generated_text" in data:
            return data["generated_text"].strip()
        else:
            logger.info("⚠️ Unexpected HF response:", data)
            return "I'm happy to proceed with this opportunity."

    except Exception as e:
        logger.info("❌ Hugging Face error:", e)
        return "I'm happy to proceed with this opportunity."
