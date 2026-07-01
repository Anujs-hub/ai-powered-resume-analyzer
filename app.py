import os
import re
import pdfplumber

from flask import Flask, render_template, request
from werkzeug.utils import secure_filename


app = Flask(__name__)


# Upload folder settings
UPLOAD_FOLDER = "uploads"

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
app.config["MAX_CONTENT_LENGTH"] = 5 * 1024 * 1024

os.makedirs(UPLOAD_FOLDER, exist_ok=True)

ALLOWED_EXTENSIONS = {"pdf"}


# Check uploaded file extension
def allowed_file(filename):

    if "." not in filename:
        return False

    extension = filename.rsplit(".", 1)[1].lower()

    return extension in ALLOWED_EXTENSIONS


# Extract text from PDF
def extract_text(pdf_path):

    text = ""

    try:

        with pdfplumber.open(pdf_path) as pdf:

            for page in pdf.pages:

                page_text = page.extract_text()

                if page_text:
                    text += page_text + "\n"

    except:
        return ""

    return text


# Skills database
skills_list = [

    # Programming
    "Python",
    "Java",
    "C++",

    # Web Development
    "HTML",
    "CSS",
    "JavaScript",

    # Databases
    "SQL",
    "MySQL",
    "MongoDB",

    # Backend
    "Flask",
    "Django",
    "REST API",

    # Data Science
    "Machine Learning",
    "Deep Learning",
    "Pandas",
    "NumPy",
    "Scikit-Learn",
    "TensorFlow",
    "PyTorch",

    # Analytics
    "Data Analysis",
    "Data Visualization",
    "Power BI",
    "Tableau",
    "Excel",

    # Tools
    "Git",
    "GitHub",
    "Linux",

    # CS Fundamentals
    "DSA",
    "OOP",

    # Cloud / DevOps
    "AWS",
    "Docker",
    "Kubernetes",

    # Others
    "API",
    "Statistics"
]


# Skill importance weights
skill_weights = {

    "Python": 5,
    "Java": 4,
    "C++": 4,

    "DSA": 5,
    "OOP": 4,

    "HTML": 2,
    "CSS": 2,
    "JavaScript": 3,

    "SQL": 4,
    "MySQL": 3,
    "MongoDB": 3,

    "Flask": 3,
    "Django": 4,
    "REST API": 3,

    "Machine Learning": 5,
    "Deep Learning": 5,
    "Pandas": 4,
    "NumPy": 3,
    "Scikit-Learn": 4,
    "TensorFlow": 5,
    "PyTorch": 5,

    "Data Analysis": 4,
    "Data Visualization": 3,
    "Power BI": 3,
    "Tableau": 3,
    "Excel": 2,

    "Git": 2,
    "GitHub": 2,
    "Linux": 2,

    "AWS": 4,
    "Docker": 4,
    "Kubernetes": 5
}
# Role wise required skills

role_skills = {

    "Software Engineer": [
        "Python",
        "Java",
        "C++",
        "DSA",
        "OOP",
        "Git",
        "GitHub",
        "SQL",
        "HTML",
        "CSS",
        "JavaScript"
    ],

    "Frontend Developer": [
        "HTML",
        "CSS",
        "JavaScript",
        "Git",
        "GitHub"
    ],

    "Backend Developer": [
        "Python",
        "SQL",
        "Flask",
        "Django",
        "REST API",
        "Git",
        "GitHub"
    ],

    "Full Stack Developer": [
        "HTML",
        "CSS",
        "JavaScript",
        "Python",
        "Flask",
        "SQL",
        "Git",
        "GitHub"
    ],

    "Python Developer": [
        "Python",
        "Flask",
        "Django",
        "SQL",
        "Git",
        "GitHub"
    ],

    "Data Analyst": [
        "Python",
        "SQL",
        "Excel",
        "Pandas",
        "NumPy",
        "Data Analysis",
        "Data Visualization",
        "Power BI",
        "Tableau"
    ],

    "Data Scientist": [
        "Python",
        "Machine Learning",
        "Pandas",
        "NumPy",
        "Scikit-Learn",
        "TensorFlow",
        "SQL",
        "Data Analysis"
    ],

    "Machine Learning Engineer": [
        "Python",
        "SQL",
        "Machine Learning",
        "Pandas",
        "NumPy",
        "Scikit-Learn",
        "TensorFlow",
        "Git",
        "Flask"
    ],

    "AI Engineer": [
        "Python",
        "Machine Learning",
        "Deep Learning",
        "TensorFlow",
        "PyTorch",
        "Pandas",
        "NumPy"
    ]
}


# Detect skills from text

def detect_skills(text):

    found_skills = []

    text = text.lower()

    for skill in skills_list:

        pattern = r"\b" + re.escape(skill.lower()) + r"\b"

        if re.search(pattern, text):
            found_skills.append(skill)

    return found_skills


# Find missing skills

def get_missing_skills(found_skills, required_skills):

    missing = []

    for skill in required_skills:

        if skill not in found_skills:
            missing.append(skill)

    return missing


# Generate recommendations

def get_recommendations(missing_skills):

    recommendations = []

    for skill in missing_skills:

        recommendations.append(
            f"Learn {skill} and add a project related to it."
        )

    return recommendations


# Extract skills from Job Description

def extract_jd_skills(job_description):

    jd_skills = []

    if not job_description:
        return jd_skills

    job_description = job_description.lower()

    for skill in skills_list:

        pattern = r"\b" + re.escape(skill.lower()) + r"\b"

        if re.search(pattern, job_description):
            jd_skills.append(skill)

    return jd_skills


# Resume vs Job Description matching

def calculate_jd_match(resume_skills, jd_skills):

    if len(jd_skills) == 0:
        return 0, []

    matched = []

    for skill in jd_skills:

        if skill in resume_skills:
            matched.append(skill)

    match_percentage = round(
        (len(matched) / len(jd_skills)) * 100,
        1
    )

    return match_percentage, matched
# Detect resume sections

def detect_sections(text):

    text = text.lower()

    sections = {

        "Education":
            "education" in text or
            "b.tech" in text or
            "bachelor" in text,

        "Projects":
            "project" in text or
            "projects" in text,

        "Experience":
            "experience" in text or
            "internship" in text,

        "Certifications":
            "certification" in text or
            "certifications" in text or
            "coursera" in text or
            "nptel" in text,

        "Skills":
            "skills" in text or
            "technical skills" in text
    }

    return sections


# Detect formatting

def detect_formatting(text):

    formatting = {}

    formatting["Email"] = bool(
        re.search(
            r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}",
            text
        )
    )

    formatting["Phone"] = bool(
        re.search(
            r"(\+91[- ]?)?[6-9]\d{9}",
            text
        )
    )

    formatting["LinkedIn"] = (
        "linkedin.com" in text.lower()
    )

    formatting["GitHub"] = (
        "github.com" in text.lower()
    )

    return formatting


# ATS Friendly Check

def check_ats_friendly(text):

    score = 0

    if re.search(
        r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}",
        text
    ):
        score += 1

    if re.search(
        r"(\+91[- ]?)?[6-9]\d{9}",
        text
    ):
        score += 1

    if "linkedin.com" in text.lower():
        score += 1

    if "github.com" in text.lower():
        score += 1

    if "project" in text.lower():
        score += 1

    return score >= 4


# Achievement Detection

def detect_achievements(text):

    pattern = (
        r"\d+(\.\d+)?\s*"
        r"(%|percent|x|times|"
        r"users|projects|clients|"
        r"accuracy|cgpa|cpi)"
    )

    achievements = re.findall(
        pattern,
        text.lower()
    )

    return len(achievements)


# Resume Completeness

def calculate_completeness(sections, formatting):

    total = 0

    total += sum(sections.values())

    total += sum(formatting.values())

    percentage = round(
        (total / 9) * 100,
        1
    )

    return min(percentage, 100)


# Resume Rank

def calculate_rank(score):

    if score >= 90:
        return "A+ Grade Resume"

    elif score >= 80:
        return "A Grade Resume"

    elif score >= 70:
        return "B Grade Resume"

    elif score >= 60:
        return "C Grade Resume"

    else:
        return "Needs Improvement"


# Keyword Density Score

def calculate_keyword_density(
        text,
        required_skills):

    text = text.lower()

    density_score = 0

    for skill in required_skills:

        count = text.count(
            skill.lower()
        )

        if count >= 3:
            density_score += 1

        elif count >= 1:
            density_score += 0.5

    if len(required_skills) == 0:
        return 0

    density_score = (
        density_score
        /
        len(required_skills)
    ) * 10

    return round(
        min(density_score, 10),
        1
    )


# Resume Strengths

def get_strengths(
        score,
        found_skills,
        sections):

    strengths = []

    if score >= 80:
        strengths.append(
            "Strong ATS Score"
        )

    if "Python" in found_skills:
        strengths.append(
            "Good Programming Skills"
        )

    if sections["Projects"]:
        strengths.append(
            "Projects Section Present"
        )

    if sections["Experience"]:
        strengths.append(
            "Experience Section Present"
        )

    if len(found_skills) >= 8:
        strengths.append(
            "Good Skill Coverage"
        )

    return strengths


# Areas to Improve

def get_weaknesses(
        score,
        missing,
        sections,
        formatting):

    weaknesses = []

    if score < 70:
        weaknesses.append(
            "Low ATS Score"
        )

    for skill in missing:
        weaknesses.append(
            f"Add {skill}"
        )

    if not sections["Projects"]:
        weaknesses.append(
            "Add Projects Section"
        )

    if not sections["Experience"]:
        weaknesses.append(
            "Add Internship or Experience"
        )

    if not formatting["LinkedIn"]:
        weaknesses.append(
            "Add LinkedIn Profile"
        )

    if not formatting["GitHub"]:
        weaknesses.append(
            "Add GitHub Profile"
        )

    return weaknesses
# Home Page

@app.route("/")
def home():

    return render_template("index.html")


# Resume Analysis

@app.route("/analyze", methods=["POST"])
def analyze():

    if "resume" not in request.files:
        return render_template("index.html")

    file = request.files["resume"]
    role = request.form.get("role")
    job_description = request.form.get("job_description", "")

    if file.filename == "":
        return render_template("index.html")

    if not allowed_file(file.filename):
        return render_template("index.html")

    filename = secure_filename(file.filename)

    filepath = os.path.join(
        app.config["UPLOAD_FOLDER"],
        filename
    )

    file.save(filepath)

    text = extract_text(filepath)

    os.remove(filepath)

    if text == "":
        return render_template("index.html")


    # Skills Analysis

    found_skills = detect_skills(text)

    required_skills = role_skills.get(
        role,
        []
    )

    missing = get_missing_skills(
        found_skills,
        required_skills
    )

    recommendations = get_recommendations(
        missing
    )


    # Job Description Match

    jd_skills = extract_jd_skills(
        job_description
    )

    resume_match, matched_jd = (
        calculate_jd_match(
            found_skills,
            jd_skills
        )
    )


    # Resume Analysis

    sections = detect_sections(
        text
    )

    formatting = detect_formatting(
        text
    )

    ats_friendly = (
        check_ats_friendly(
            text
        )
    )

    achievement_count = (
        detect_achievements(
            text
        )
    )

    completeness = (
        calculate_completeness(
            sections,
            formatting
        )
    )

    density_score = (
        calculate_keyword_density(
            text,
            required_skills
        )
    )


    # Skills Score (35)

    matched = 0
    matched_weight = 0
    total_weight = 0

    for skill in required_skills:

        weight = skill_weights.get(
            skill,
            1
        )

        total_weight += weight

        if skill in found_skills:

            matched += 1
            matched_weight += weight

    skills_score = 0

    if total_weight > 0:

        skills_score = (
            matched_weight /
            total_weight
        ) * 35


    # Section Score (20)

    section_score = 0

    if sections["Education"]:
        section_score += 4

    if sections["Projects"]:
        section_score += 5

    if sections["Experience"]:
        section_score += 5

    if sections["Certifications"]:
        section_score += 3

    if sections["Skills"]:
        section_score += 3


    # Formatting Score (15)

    formatting_score = (
        sum(
            formatting.values()
        ) * 3
    )

    if ats_friendly:
        formatting_score += 3

    formatting_score = min(
        formatting_score,
        15
    )


    # Experience Score (10)

    experience_score = 0

    if "internship" in text.lower():
        experience_score += 5

    if "experience" in text.lower():
        experience_score += 5


    # Achievement Score (10)

    achievement_score = min(
        achievement_count,
        10
    )


    # Final ATS Score

    score = int(

        skills_score
        +
        section_score
        +
        formatting_score
        +
        experience_score
        +
        achievement_score
        +
        density_score
    )

    score = min(score, 100)


    # Keyword Match %

    match_percentage = 0

    if len(required_skills) > 0:

        match_percentage = round(

            (
                matched
                /
                len(required_skills)
            ) * 100,

            1
        )


    # Resume Rank

    rank = calculate_rank(
        score
    )


    # Strengths & Weaknesses

    strengths = get_strengths(
        score,
        found_skills,
        sections
    )

    weaknesses = get_weaknesses(
        score,
        missing,
        sections,
        formatting
    )


    return render_template(

        "result.html",

        role=role,

        score=score,

        skills=found_skills,

        missing=missing,

        recommendations=recommendations,

        sections=sections,

        formatting=formatting,

        strengths=strengths,

        weaknesses=weaknesses,

        resume_preview=text[:500],

        achievement_count=achievement_count,

        matched=matched,

        total_required=len(
            required_skills
        ),

        match_percentage=
            match_percentage,

        skills_score=
            round(skills_score,1),

        section_score=
            round(section_score,1),

        formatting_score=
            round(formatting_score,1),

        experience_score=
            round(experience_score,1),

        achievement_score=
            round(achievement_score,1),

        density_score=
            round(density_score,1),

        completeness=
            completeness,

        rank=
            rank,

        ats_friendly=
            ats_friendly,

        resume_match=
            resume_match,

        jd_skills=
            jd_skills,

        matched_jd=
            matched_jd
    )


if __name__ == "__main__":

    app.run(debug=True)
    