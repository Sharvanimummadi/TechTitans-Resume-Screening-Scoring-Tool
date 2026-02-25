from flask import Flask, render_template, request
import PyPDF2

app = Flask(__name__)

# Job Role Data
job_roles = {
    "Python Developer": {
        "skills": ["python", "flask", "django", "mysql", "api"],
        "top_companies": [
            {"name": "Google", "link": "https://careers.google.com"},
            {"name": "Amazon", "link": "https://amazon.jobs"},
            {"name": "Infosys", "link": "https://www.infosys.com/careers"}
        ],
        "mid_companies": [
            {"name": "TCS", "link": "https://www.tcs.com/careers"},
            {"name": "Wipro", "link": "https://careers.wipro.com"}
        ]
    },
    "Java Developer": {
        "skills": ["java", "spring", "hibernate", "mysql", "rest"],
        "top_companies": [
            {"name": "Oracle", "link": "https://www.oracle.com/careers"},
            {"name": "Capgemini", "link": "https://www.capgemini.com/careers"},
            {"name": "Accenture", "link": "https://www.accenture.com/careers"}
        ],
        "mid_companies": [
            {"name": "Cognizant", "link": "https://careers.cognizant.com"},
            {"name": "HCL", "link": "https://www.hcltech.com/careers"}
        ]
    },
    "Web Developer": {
        "skills": ["html", "css", "javascript", "react", "node"],
        "top_companies": [
            {"name": "Meta", "link": "https://www.metacareers.com"},
            {"name": "Adobe", "link": "https://www.adobe.com/careers"},
            {"name": "Flipkart", "link": "https://www.flipkartcareers.com"}
        ],
        "mid_companies": [
            {"name": "Zoho", "link": "https://www.zoho.com/careers"},
            {"name": "Freshworks", "link": "https://www.freshworks.com/company/careers"}
        ]
    }
}

def extract_text_from_pdf(file):
    reader = PyPDF2.PdfReader(file)
    text = ""
    for page in reader.pages:
        text += page.extract_text()
    return text.lower()

def get_company_recommendations(score, job_data):
    if score >= 80:
        return job_data["top_companies"]
    elif score >= 40:
        return job_data["mid_companies"]
    else:
        return [{"name": "Start with Internships",
                 "link": "https://internshala.com"}]

@app.route("/", methods=["GET", "POST"])
def index():
    score = None
    matched = []
    missing = []
    companies = []
    roadmap = []

    if request.method == "POST":
        job_role = request.form["job_role"]
        resume = request.files["resume"]

        if resume:
            resume_text = extract_text_from_pdf(resume)
            required_skills = job_roles[job_role]["skills"]

            matched = [skill for skill in required_skills if skill in resume_text]
            missing = [skill for skill in required_skills if skill not in resume_text]

            score = int((len(matched) / len(required_skills)) * 100)

            companies = get_company_recommendations(score, job_roles[job_role])

            for skill in missing:
                roadmap.append({
                    "skill": skill,
                    "plan": [
                        f"Week 1-2: Learn basics of {skill}",
                        f"Week 3: Build mini project using {skill}",
                        f"Week 4: Add {skill} project to resume"
                    ]
                })

    return render_template("index.html",
                           jobs=job_roles.keys(),
                           score=score,
                           matched=matched,
                           missing=missing,
                           companies=companies,
                           roadmap=roadmap)

if __name__ == "__main__":
    app.run(debug=True)