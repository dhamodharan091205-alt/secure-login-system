import re

def extract_text_from_pdf(file_bytes):
    import pdfplumber
    import io
    text = ""
    with pdfplumber.open(io.BytesIO(file_bytes)) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"
    return text

def extract_text_from_docx(file_bytes):
    import docx
    import io
    doc = docx.Document(io.BytesIO(file_bytes))
    text = ""
    for para in doc.paragraphs:
        text += para.text + "\n"
    return text

def parse_resume(text):
    # Email
    email_match = re.search(r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}', text)
    email = email_match.group(0) if email_match else None

    # Phone - Indian + International format
    phone_match = re.search(r'(\+91[\s-]?)?[6-9]\d{9}|\+\d{1,3}[\s-]?\d{6,14}', text)
    phone = phone_match.group(0) if phone_match else None

    # Name - first line
    lines = [line.strip() for line in text.split('\n') if line.strip()]
    name = lines[0] if lines else None
    if name and len(name) > 50:
        name = name[:50]

    # Skills - common skills list
    common_skills = [
        "python", "java", "javascript", "typescript", "react", "angular", "vue",
        "node", "express", "django", "flask", "fastapi", "sql", "mysql",
        "postgresql", "mongodb", "html", "css", "aws", "azure", "docker",
        "kubernetes", "git", "machine learning", "deep learning", "pandas",
        "numpy", "tensorflow", "pytorch", "excel", "power bi", "c++", "c#",
        "php", "ruby", "go", "rust", "spring", "hibernate", "rest api"
    ]
    text_lower = text.lower()
    found_skills = [skill for skill in common_skills if skill in text_lower]

    # Experience and Education - simple split
    experience = ""
    education = ""
    if "experience" in text_lower:
        start = text_lower.find("experience")
        experience = text[start:start+1500]
    if "education" in text_lower:
        start = text_lower.find("education")
        education = text[start:start+1000]

    return {
        "name": name,
        "email": email,
        "phone": phone,
        "skills": ", ".join(found_skills),
        "experience": experience,
        "education": education,
        "raw_text": text
    }

def calculate_match(resume_skills, jd_text):
    jd_lower = jd_text.lower()
    resume_skill_list = [s.strip().lower() for s in resume_skills.split(",") if s.strip()] if resume_skills else []

    matched = []
    missing = []

    # Find skills from JD
    common_skills = [
        "python", "java", "javascript", "typescript", "react", "angular", "vue",
        "node", "express", "django", "flask", "fastapi", "sql", "mysql",
        "postgresql", "mongodb", "html", "css", "aws", "azure", "docker",
        "kubernetes", "git", "machine learning", "deep learning", "pandas",
        "numpy", "tensorflow", "pytorch", "excel", "power bi", "c++", "c#",
        "php", "ruby", "go", "rust", "spring", "hibernate", "rest api"
    ]

    jd_skills = [skill for skill in common_skills if skill in jd_lower]

    if not jd_skills:
        return 0, "", ""

    for skill in jd_skills:
        if skill in resume_skill_list:
            matched.append(skill)
        else:
            missing.append(skill)

    score = int((len(matched) / len(jd_skills)) * 100)

    return score, ", ".join(matched), ", ".join(missing)