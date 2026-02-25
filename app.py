from flask import Flask, render_template, request, redirect, url_for, session
import PyPDF2

app = Flask(__name__)
app.secret_key = "techtitans_secret"

# =========================
# JOB DATABASE
# =========================

job_roles = {

    "Python Developer": {
        "skills": ["python", "flask", "django", "mysql", "api"],
        "companies": {
            "high": ["Google", "Amazon", "Microsoft"],
            "medium": ["TCS", "Infosys", "Wipro"],
            "low": ["Python Internship Programs"]
        },
        "certifications": [
            "PCAP: Certified Associate in Python",
            "Google IT Automation with Python",
            "Python for Everybody - Coursera"
        ]
    },

    "Java Developer": {
        "skills": ["java", "spring", "hibernate", "mysql", "rest"],
        "companies": {
            "high": ["Accenture", "IBM"],
            "medium": ["HCL", "Capgemini"],
            "low": ["Java Internship Programs"]
        },
        "certifications": [
            "Oracle Certified Java Programmer",
            "Spring Professional Certification"
        ]
    },

    "Web Developer": {
        "skills": ["html", "css", "javascript", "react", "node"],
        "companies": {
            "high": ["Zoho", "Freshworks"],
            "medium": ["Tech Mahindra"],
            "low": ["Frontend Internship"]
        },
        "certifications": [
            "Meta Front-End Developer Certificate",
            "Full Stack Web Development - Udemy"
        ]
    },

    "Data Analyst": {
        "skills": ["python", "sql", "excel", "powerbi", "tableau"],
        "companies": {
            "high": ["Deloitte", "EY", "KPMG"],
            "medium": ["Infosys Analytics"],
            "low": ["Data Analyst Internship"]
        },
        "certifications": [
            "Google Data Analytics Certificate",
            "Microsoft Power BI Certification"
        ]
    },

    "Machine Learning Engineer": {
        "skills": ["python", "numpy", "pandas", "sklearn", "tensorflow"],
        "companies": {
            "high": ["NVIDIA", "Amazon AI", "Google AI"],
            "medium": ["TCS AI Division"],
            "low": ["ML Internship"]
        },
        "certifications": [
            "Machine Learning by Andrew Ng",
            "TensorFlow Developer Certificate"
        ]
    }
}

# =========================
# LEARNING PATHS
# =========================

learning_paths = {
    "python": "Complete Python basics and build mini projects.",
    "flask": "Build REST APIs using Flask.",
    "django": "Create a blog project using Django.",
    "mysql": "Practice SQL queries daily.",
    "api": "Build CRUD REST API project.",
    "java": "Revise OOP and collections.",
    "spring": "Build Spring Boot project.",
    "hibernate": "Learn ORM mapping.",
    "rest": "Build RESTful services.",
    "html": "Build static portfolio website.",
    "css": "Learn Flexbox & Grid.",
    "javascript": "Practice DOM projects.",
    "react": "Create React ToDo app.",
    "node": "Build backend using Express.",
    "sql": "Practice advanced joins.",
    "excel": "Learn pivot tables & dashboards.",
    "powerbi": "Create Power BI dashboard.",
    "tableau": "Build data visualization project.",
    "numpy": "Learn numerical computing.",
    "pandas": "Practice data cleaning.",
    "sklearn": "Build ML model using sklearn.",
    "tensorflow": "Build neural network project."
}

# =========================
# ROUTES
# =========================

@app.route('/')
def home():
    return render_template("home.html")


@app.route('/upload')
def upload():
    return render_template("upload.html", jobs=job_roles.keys())


@app.route('/analyze', methods=['POST'])
def analyze():
    selected_job = request.form['job_role']
    file = request.files['resume']

    if not file:
        return redirect(url_for('upload'))

    reader = PyPDF2.PdfReader(file)
    text = ""

    for page in reader.pages:
        extracted = page.extract_text()
        if extracted:
            text += extracted.lower()

    required_skills = job_roles[selected_job]["skills"]

    matched = []
    missing = []

    for skill in required_skills:
        if skill in text:
            matched.append(skill)
        else:
            missing.append(skill)

    score = int((len(matched) / len(required_skills)) * 100)

    if score >= 80:
        recommended = job_roles[selected_job]["companies"]["high"]
    elif score >= 40:
        recommended = job_roles[selected_job]["companies"]["medium"]
    else:
        recommended = job_roles[selected_job]["companies"]["low"]

    session['missing'] = missing
    session['improvement'] = {
        skill: learning_paths.get(skill, "Practice and build projects.")
        for skill in missing
    }
    session['certifications'] = job_roles[selected_job]["certifications"]

    return render_template("result.html",
                           score=score,
                           matched=matched,
                           companies=recommended)


@app.route('/improvement')
def improvement():
    return render_template("improvement.html",
                           missing=session.get('missing', []),
                           improvement=session.get('improvement', {}),
                           certifications=session.get('certifications', []))


if __name__ == "__main__":
    app.run(debug=True)