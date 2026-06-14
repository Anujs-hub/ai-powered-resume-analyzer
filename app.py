import pdfplumber
from flask import Flask, render_template, request
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
def extract_text(pdf_path):

    text = ""

    with pdfplumber.open(pdf_path) as pdf:

        for page in pdf.pages:

            page_text = page.extract_text()

            if page_text:
                text += page_text

    return text

skills_list = [
    "Python",
    "C++",
    "Java",
    "JavaScript",
    "HTML",
    "CSS",
    "Git",
    "GitHub",
    "SQL",
    "Excel",
    "Machine Learning",
    "Deep Learning",
    "Data Analysis",
    "Data Visualization",
    "Pandas",
    "NumPy",
    "Scikit-Learn",
    "TensorFlow",
    "PyTorch",
    "Flask",
    "Django",
    "REST API",
    "MySQL",
    "MongoDB",
    "Power BI",
    "Tableau",
    "Linux",
    "OOP",
    "DSA"
]
def detect_skills(text):

    found_skills = []

    for skill in skills_list:

        if skill.lower() in text.lower():

            found_skills.append(skill)

    return found_skills
def missing_skills(found_skills, required_skills):

    missing = []

    for skill in required_skills:

        if skill not in found_skills:

            missing.append(skill)

    return missing
def get_recommendations(missing):

    recommendations = []

    for skill in missing:
        recommendations.append(
            f"Learn {skill} and add a project using it."
        )

    return recommendations
def detect_sections(text):

    sections = {}

    sections["Education"] = (
        "education" in text.lower()
        or "b.tech" in text.lower()
        or "bachelor" in text.lower()
    )

    sections["Projects"] = (
        "project" in text.lower()
        or "projects" in text.lower()
    )

    sections["Experience"] = (
        "experience" in text.lower()
        or "internship" in text.lower()
    )

    sections["Certifications"] = (
        "certification" in text.lower()
        or "certifications" in text.lower()
        or "nptel" in text.lower()
        or "coursera" in text.lower()
    )

    return sections
def get_strengths(score, found_skills, sections):

    strengths = []

    if score >= 70:
        strengths.append("Good ATS Score")

    if "Python" in found_skills:
        strengths.append("Strong Python Skills")

    if sections.get("Projects"):
        strengths.append("Projects Section Present")

    return strengths
def get_weaknesses(missing, sections):

    weaknesses = []

    for skill in missing:
        weaknesses.append(f"Missing {skill}")

    if not sections.get("Projects"):
        weaknesses.append("Projects Section Missing")

    if not sections.get("Experience"):
        weaknesses.append("Experience Section Missing")

    return weaknesses
@app.route("/", methods=["GET", "POST"])
def home():

    message = ""
    found_skills = []
    score = 0
    missing = []
    recommendations = []
    role = ""
    sections={}
    strengths=[]
    weaknesses=[]
    resume_preview=""
    matched=0
    total_required=0

    if request.method == "POST":

        if "resume" not in request.files:
            message = "No file selected"

        else:
            role = request.form["role"]
            file = request.files["resume"]
            

            if file.filename == "":
                message = "Please choose a PDF"

            else:

                filename = secure_filename(file.filename)
                


            pdf_path = os.path.join(app.config["UPLOAD_FOLDER"],filename)
            file.save(pdf_path)
            text = extract_text(pdf_path)
            resume_preview = text[:500]
            sections = detect_sections(text)


            print("\n===== RESUME TEXT =====\n")
            print(text)
            found_skills = detect_skills(text)
            if role == "ML Engineer":

                required_skills = [
                        "Python",
                        "SQL",
                        "Machine Learning",
                        "Pandas",
                        "NumPy",
                        "Scikit-Learn",
                        "TensorFlow",
                        "Git",
                        "Flask"
                    ]          
            elif role == "Data Analyst":
                   required_skills = [
                       "Python",
                       "SQL",
                       "Excel",
                       "Pandas",
                       "NumPy",
                       "Data Analysis",
                       "Data Visualization",
                       "Power BI",
                       "Tableau"
                   ]
            else:
                required_skills = [
                    "Python",
                    "C++",
                    "Java",
                    "OOP",
                    "DSA",
                    "Git",
                    "GitHub",
                    "SQL",
                    "HTML",
                    "CSS",
                    "JavaScript"
                ]                
            print("\n===== DETECTED SKILLS =====\n")
            print(found_skills)
            missing = missing_skills(found_skills, required_skills)
            recommendations = get_recommendations(missing)

            matched = 0

            for skill in required_skills:
                if skill in found_skills:
                    matched += 1

            skills_score = (matched / len(required_skills)) * 60

            section_score = 0

            if sections.get("Projects"):
                section_score += 20

            if sections.get("Experience"):
                section_score += 10
            
            if sections.get("Certifications"):
                section_score += 10

            score = int(skills_score + section_score)            

            strengths = get_strengths(
                score,
                found_skills,
                sections
            )

            weaknesses = get_weaknesses(
                missing,
                sections
            )
            print("\n===== ATS SCORE =====\n")
            print(score)


            message = f"{filename} uploaded successfully"
            return render_template(

                "result.html",
                skills=found_skills,
                score=score,
                missing=missing,
                recommendations=recommendations,
                role=role,
                sections=sections,
                strengths=strengths,
                weaknesses=weaknesses,
                resume_preview=resume_preview,
                matched=matched,
                total_required=len(required_skills)
            )


    return render_template(
        "index.html",
        skills=found_skills,
        score=score,
        missing=missing,
        recommendations=recommendations,
        role=role,
        sections=sections,
        strengths=strengths,
        weaknesses=weaknesses,
        resume_preview=resume_preview,
        matched=matched,
        total_required=total_required
    )    
if __name__ == "__main__":
    app.run(debug=True)