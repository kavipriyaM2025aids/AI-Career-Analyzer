from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
import re

app = FastAPI(title="AI Career Analyzer API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

USERS = {
    "admin": "admin123",
    "user": "user123",
}

CAREER_DATA = {
    "Data Scientist": {
        "demand": 92, "automation_risk": 15, "stability": 88,
        "salary": "₹10,00,000 - ₹25,00,000 LPA",
        "required_skills": ["Python", "Machine Learning", "Statistics", "SQL",
                             "Data Visualization", "Deep Learning", "TensorFlow",
                             "R", "Pandas", "NumPy"],
        "resources": [
            {"name": "SWAYAM - Data Science for Engineers", "url": "https://swayam.gov.in/nd1_noc20_cs60/preview"},
            {"name": "Coursera - Data Science Specialization", "url": "https://www.coursera.org/specializations/jhu-data-science"},
            {"name": "Great Learning - Free Data Science Course", "url": "https://www.mygreatlearning.com/academy/learn-for-free/courses/introduction-to-data-science"},
            {"name": "Udemy - Data Science Bootcamp", "url": "https://www.udemy.com/course/python-for-data-science-and-machine-learning-bootcamp/"},
        ]
    },
    "Software Engineer": {
        "demand": 88, "automation_risk": 20, "stability": 85,
        "salary": "₹8,00,000 - ₹30,00,000 LPA",
        "required_skills": ["Java", "Python", "Data Structures", "Algorithms",
                             "System Design", "Git", "SQL", "REST APIs", "Cloud", "Docker"],
        "resources": [
            {"name": "LeetCode - DSA Practice", "url": "https://leetcode.com/problemset/"},
            {"name": "Coursera - Software Engineering", "url": "https://www.coursera.org/specializations/software-engineering"},
            {"name": "Udemy - Full Stack Development", "url": "https://www.udemy.com/course/the-complete-web-development-bootcamp/"},
            {"name": "freeCodeCamp", "url": "https://www.freecodecamp.org/learn"},
        ]
    },
    "Cybersecurity Analyst": {
        "demand": 95, "automation_risk": 10, "stability": 90,
        "salary": "₹6,00,000 - ₹20,00,000 LPA",
        "required_skills": ["Network Security", "Ethical Hacking", "Linux",
                             "Python", "Firewall", "SIEM", "Cryptography",
                             "Penetration Testing", "Incident Response", "Compliance"],
        "resources": [
            {"name": "Coursera - IBM Cybersecurity Analyst", "url": "https://www.coursera.org/professional-certificates/ibm-cybersecurity-analyst"},
            {"name": "Udemy - Cyber Security Course", "url": "https://www.udemy.com/course/the-complete-internet-security-privacy-course-volume-1/"},
            {"name": "Great Learning - Introduction to Cyber Security", "url": "https://www.mygreatlearning.com/academy/learn-for-free/courses/introduction-to-cyber-security"},
            {"name": "SWAYAM - Introduction to Cyber Security", "url": "https://swayam.gov.in/nd2_cec20_cs03/preview"},
        ]
    },
    "Cloud Architect": {
        "demand": 90, "automation_risk": 18, "stability": 87,
        "salary": "₹15,00,000 - ₹40,00,000 LPA",
        "required_skills": ["AWS", "Azure", "GCP", "Kubernetes", "Docker",
                             "Terraform", "Networking", "Security", "Python", "DevOps"],
        "resources": [
            {"name": "AWS Training", "url": "https://explore.skillbuilder.aws/learn"},
            {"name": "Google Cloud Skills Boost", "url": "https://www.cloudskillsboost.google/paths/12"},
            {"name": "Coursera - AWS Cloud Solutions Architect", "url": "https://www.coursera.org/professional-certificates/aws-cloud-solutions-architect"},
            {"name": "Udemy - AWS Certified Solutions Architect", "url": "https://www.udemy.com/course/aws-certified-solutions-architect-associate-saa-c03/"},
        ]
    },
    "UX Designer": {
        "demand": 80, "automation_risk": 25, "stability": 78,
        "salary": "₹5,00,000 - ₹18,00,000 LPA",
        "required_skills": ["Figma", "User Research", "Wireframing", "Prototyping",
                             "Adobe XD", "HTML/CSS", "Accessibility", "Usability Testing",
                             "Design Systems", "Sketch"],
        "resources": [
            {"name": "Coursera - Google UX Design", "url": "https://www.coursera.org/professional-certificates/google-ux-design"},
            {"name": "Interaction Design Foundation", "url": "https://www.interaction-design.org/courses"},
            {"name": "Udemy - UX Design Bootcamp", "url": "https://www.udemy.com/course/ui-ux-web-design-using-adobe-xd/"},
            {"name": "SWAYAM - UI/UX Design", "url": "https://swayam.gov.in/nd1_noc20_cs69/preview"},
        ]
    },
    "DevOps Engineer": {
        "demand": 89, "automation_risk": 22, "stability": 86,
        "salary": "₹8,00,000 - ₹28,00,000 LPA",
        "required_skills": ["Docker", "Kubernetes", "Jenkins", "CI/CD", "Linux",
                             "Python", "Terraform", "AWS", "Monitoring", "Git"],
        "resources": [
            {"name": "SWAYAM - Cloud Computing & DevOps", "url": "https://swayam.gov.in/nd1_noc20_cs79/preview"},
            {"name": "Coursera - DevOps on AWS", "url": "https://www.coursera.org/specializations/aws-devops"},
            {"name": "Udemy - Docker & Kubernetes", "url": "https://www.udemy.com/course/docker-and-kubernetes-the-complete-guide/"},
            {"name": "Great Learning - DevOps Course", "url": "https://www.mygreatlearning.com/academy/learn-for-free/courses/devops-fundamentals"},
        ]
    },
    "AI/ML Engineer": {
        "demand": 96, "automation_risk": 12, "stability": 91,
        "salary": "₹12,00,000 - ₹40,00,000 LPA",
        "required_skills": ["Python", "TensorFlow", "PyTorch", "Machine Learning",
                             "Deep Learning", "NLP", "Computer Vision", "MLOps",
                             "Statistics", "Data Engineering"],
        "resources": [
            {"name": "SWAYAM - Artificial Intelligence Course", "url": "https://swayam.gov.in/nd1_noc20_cs63/preview"},
            {"name": "Coursera - DeepLearning.AI", "url": "https://www.coursera.org/specializations/deep-learning"},
            {"name": "Udemy - Machine Learning A-Z", "url": "https://www.udemy.com/course/machinelearning/"},
            {"name": "Great Learning - AI & ML Course", "url": "https://www.mygreatlearning.com/academy/learn-for-free/courses/introduction-to-artificial-intelligence"},
        ]
    },
    "Product Manager": {
        "demand": 82, "automation_risk": 28, "stability": 80,
        "salary": "₹12,00,000 - ₹35,00,000 LPA",
        "required_skills": ["Product Strategy", "User Stories", "Agile", "Scrum",
                             "Data Analysis", "Roadmapping", "Stakeholder Management",
                             "SQL", "A/B Testing", "Market Research"],
        "resources": [
            {"name": "SWAYAM - Product Management Course", "url": "https://swayam.gov.in/nd2_arp19_mg33/preview"},
            {"name": "Udemy - Become a Product Manager", "url": "https://www.udemy.com/course/become-a-product-manager-learn-the-skills-get-a-job/"},
            {"name": "Great Learning - Product Management Course", "url": "https://www.mygreatlearning.com/academy/learn-for-free/courses/product-management"},
            {"name": "SWAYAM - Management Fundamentals", "url": "https://swayam.gov.in/nd1_noc20_mg30/preview"},
        ]
    },
    "Data Analyst": {
        "demand": 85, "automation_risk": 30, "stability": 82,
        "salary": "₹4,00,000 - ₹15,00,000 LPA",
        "required_skills": ["SQL", "Excel", "Python", "Tableau", "Power BI",
                             "Statistics", "Data Cleaning", "R", "Pandas", "Visualization"],
        "resources": [
            {"name": "Google Data Analytics Certificate", "url": "https://www.coursera.org/professional-certificates/google-data-analytics"},
            {"name": "Tableau Training", "url": "https://www.tableau.com/learn/training"},
            {"name": "Udemy - Data Analyst Bootcamp", "url": "https://www.udemy.com/course/data-analyst-bootcamp/"},
            {"name": "Great Learning - Data Analytics Course", "url": "https://www.mygreatlearning.com/academy/learn-for-free/courses/data-analytics"},
        ]
    },
    "Blockchain Developer": {
        "demand": 75, "automation_risk": 15, "stability": 70,
        "salary": "₹8,00,000 - ₹30,00,000 LPA",
        "required_skills": ["Solidity", "Ethereum", "Web3.js", "Smart Contracts",
                             "JavaScript", "Python", "Cryptography", "DeFi",
                             "Hyperledger", "Node.js"],
        "resources": [
            {"name": "Coursera - Blockchain Specialization", "url": "https://www.coursera.org/specializations/blockchain"},
            {"name": "Udemy - Ethereum Blockchain Developer Course", "url": "https://www.udemy.com/course/ethereum-and-solidity-the-complete-developers-guide/"},
            {"name": "Great Learning - Blockchain Course", "url": "https://www.mygreatlearning.com/academy/learn-for-free/courses/blockchain-basics"},
            {"name": "SWAYAM - Blockchain Technology", "url": "https://swayam.gov.in/nd1_noc20_cs82/preview"},
        ]
    },
    "JEE Aspirant (Engineering)": {
        "demand": 70, "automation_risk": 5, "stability": 75,
        "salary": "₹6,00,000 - ₹25,00,000 LPA",
        "required_skills": ["Mathematics", "Physics", "Chemistry", "Problem Solving",
                             "Calculus", "Mechanics", "Organic Chemistry",
                             "Trigonometry", "Thermodynamics", "Analytical Thinking"],
        "resources": [
            {"name": "Unacademy - JEE Preparation", "url": "https://unacademy.com/goal/jee-main-and-advanced-preparation/TMUVD"},
            {"name": "Vedantu - JEE Courses", "url": "https://www.vedantu.com/jee-main"},
            {"name": "Udemy - Physics for JEE", "url": "https://www.udemy.com/course/physics-for-jee-main-advanced/"},
            {"name": "SWAYAM - Engineering Mathematics", "url": "https://onlinecourses.nptel.ac.in/noc20_ma29/preview"},
        ]
    },
    "NEET Aspirant (Medical)": {
        "demand": 72, "automation_risk": 5, "stability": 80,
        "salary": "₹8,00,000 - ₹30,00,000 LPA",
        "required_skills": ["Biology", "Chemistry", "Physics", "Human Anatomy",
                             "Physiology", "Biochemistry", "Genetics", "Ecology",
                             "Organic Chemistry", "Clinical Knowledge"],
        "resources": [
            {"name": "Vedantu - NEET Preparation", "url": "https://www.vedantu.com/neet"},
            {"name": "BYJU'S NEET Course", "url": "https://byjus.com/neet/"},
            {"name": "Udemy - Biology for NEET", "url": "https://www.udemy.com/course/biology-for-neet/"},
            {"name": "SWAYAM - Human Anatomy Course", "url": "https://onlinecourses.nptel.ac.in/noc20_bt17/preview"},
        ]
    },
    "Chartered Accountant (CA)": {
        "demand": 78, "automation_risk": 35, "stability": 85,
        "salary": "₹7,00,000 - ₹25,00,000 LPA",
        "required_skills": ["Accounting", "Taxation", "Auditing", "Financial Reporting",
                             "Company Law", "GST", "Income Tax", "Excel",
                             "Tally", "Financial Analysis"],
        "resources": [
            {"name": "ICAI Official Learning Portal", "url": "https://learning.icai.org/"},
            {"name": "BYJU'S CA Foundation Course", "url": "https://byjus.com/commerce/ca-foundation/"},
            {"name": "Udemy - Accounting & Finance Course", "url": "https://www.udemy.com/course/the-complete-financial-analyst-course/"},
            {"name": "Great Learning - Accounting Course", "url": "https://www.mygreatlearning.com/academy/learn-for-free/courses/introduction-to-accounting"},
        ]
    },
    "Lawyer": {
        "demand": 74, "automation_risk": 22, "stability": 82,
        "salary": "₹5,00,000 - ₹30,00,000 LPA",
        "required_skills": ["Legal Research", "Constitutional Law", "Criminal Law",
                             "Contract Law", "Corporate Law", "Drafting",
                             "Litigation", "Negotiation", "Legal Writing", "IPC/CrPC"],
        "resources": [
            {"name": "Bar Council of India - Legal Education", "url": "https://www.barcouncilofindia.org/info/ler2019-draft-01"},
            {"name": "Coursera - A Law Student's Toolkit", "url": "https://www.coursera.org/learn/law-student"},
            {"name": "LawSikho - Law Courses", "url": "https://lawsikho.com/courses/"},
            {"name": "iPleaders - Law Notes", "url": "https://blog.ipleaders.in/category/law-notes/"},
        ]
    },
    "Civil Services (UPSC Aspirant)": {
        "demand": 65, "automation_risk": 8, "stability": 95,
        "salary": "₹6,00,000 - ₹20,00,000 LPA",
        "required_skills": ["General Studies", "Indian Polity", "History", "Geography",
                             "Economics", "Current Affairs", "Essay Writing",
                             "Ethics", "Optional Subject", "Analytical Reasoning"],
        "resources": [
            {"name": "Unacademy - UPSC CSE Preparation", "url": "https://unacademy.com/goal/upsc-civil-services-examination-ias-preparation/KSCGY"},
            {"name": "Vision IAS - UPSC Courses", "url": "https://www.visionias.in/student/programmes/general-studies.php"},
            {"name": "BYJU'S IAS Preparation", "url": "https://byjus.com/free-ias-prep/"},
            {"name": "Insights IAS - Current Affairs", "url": "https://www.insightsonindia.com/current-affairs/"},
        ]
    },
    "Entrepreneur": {
        "demand": 70, "automation_risk": 20, "stability": 60,
        "salary": "₹0 - ₹1,00,00,000+ LPA",
        "required_skills": ["Business Strategy", "Leadership", "Marketing", "Finance",
                             "Networking", "Problem Solving", "Product Development",
                             "Sales", "Operations", "Fundraising"],
        "resources": [
            {"name": "Y Combinator Startup School", "url": "https://www.startupschool.org/"},
            {"name": "Udemy - Entrepreneurship Course", "url": "https://www.udemy.com/course/entrepreneurship-from-idea-to-launch/"},
            {"name": "Great Learning - Entrepreneurship Course", "url": "https://www.mygreatlearning.com/academy/learn-for-free/courses/entrepreneurship"},
            {"name": "SWAYAM - Entrepreneurship Development", "url": "https://onlinecourses.nptel.ac.in/noc20_mg18/preview"},
        ]
    },
}


class LoginRequest(BaseModel):
    username: str
    password: str


class CareerAnalysisRequest(BaseModel):
    career: str
    skills: str  # comma-separated


def compute_skill_match(user_skills: List[str], required_skills: List[str]) -> dict:
    user_set = {s.strip().lower() for s in user_skills if s.strip()}
    required_lower = {s.lower(): s for s in required_skills}
    matched = [required_lower[r] for r in required_lower if r in user_set]
    missing = [required_lower[r] for r in required_lower if r not in user_set]
    pct = round(len(matched) / len(required_skills) * 100) if required_skills else 0
    return {"matched": matched, "missing": missing, "percentage": pct}


def generate_recommendation(career: str, match_pct: int, missing: List[str]) -> str:
    if match_pct >= 80:
        return (f"Excellent match! You have strong foundational skills for a {career} role. "
                f"Focus on deepening expertise and building portfolio projects.")
    elif match_pct >= 50:
        gap = ", ".join(missing[:3])
        return (f"Good foundation! To become a {career}, prioritize learning: {gap}. "
                f"Consider hands-on projects to bridge remaining gaps.")
    else:
        return (f"This career requires significant upskilling. Start with foundational courses "
                f"in the core skills and build incrementally toward a {career} role.")


def extract_skills_from_text(text: str) -> List[str]:
    all_skills = set()
    for career in CAREER_DATA.values():
        all_skills.update(career["required_skills"])
    text_lower = text.lower()
    found = [s for s in all_skills if s.lower() in text_lower]
    return found


@app.get("/")
def root():
    return {"message": "AI Career Analyzer API is running"}


@app.post("/api/login")
def login(req: LoginRequest):
    if req.username in USERS and USERS[req.username] == req.password:
        return {"success": True, "username": req.username, "token": f"token_{req.username}"}
    raise HTTPException(status_code=401, detail="Invalid username or password")


@app.get("/api/careers")
def get_careers():
    return {"careers": list(CAREER_DATA.keys())}


@app.post("/api/analyze-career")
def analyze_career(req: CareerAnalysisRequest):
    if req.career not in CAREER_DATA:
        raise HTTPException(status_code=404, detail="Career not found")

    data = CAREER_DATA[req.career]
    user_skills = [s.strip() for s in req.skills.split(",") if s.strip()]
    skill_info = compute_skill_match(user_skills, data["required_skills"])
    recommendation = generate_recommendation(req.career, skill_info["percentage"], skill_info["missing"])

    return {
        "career": req.career,
        "demand": data["demand"],
        "automation_risk": data["automation_risk"],
        "stability": data["stability"],
        "salary": data["salary"],
        "skill_match_percentage": skill_info["percentage"],
        "matched_skills": skill_info["matched"],
        "missing_skills": skill_info["missing"],
        "recommendation": recommendation,
        "resources": data["resources"],
    }


@app.post("/api/analyze-resume")
async def analyze_resume(file: UploadFile = File(...)):
    if not file.filename.endswith((".pdf", ".txt")):
        raise HTTPException(status_code=400, detail="Only PDF and TXT files are supported")

    content = await file.read()
    try:
        text = content.decode("utf-8", errors="ignore")
    except Exception:
        text = ""

    detected_skills = extract_skills_from_text(text)

    # Score each career
    career_scores = []
    for career_name, data in CAREER_DATA.items():
        skill_info = compute_skill_match(detected_skills, data["required_skills"])
        career_scores.append({
            "career": career_name,
            "match_percentage": skill_info["percentage"],
            "matched_skills": skill_info["matched"],
        })

    career_scores.sort(key=lambda x: x["match_percentage"], reverse=True)
    top_career = career_scores[0]["career"] if career_scores else None
    top_data = CAREER_DATA.get(top_career, {})
    top_skill_info = compute_skill_match(detected_skills, top_data.get("required_skills", []))

    recommendation = generate_recommendation(
        top_career, top_skill_info["percentage"], top_skill_info["missing"]
    ) if top_career else "Upload a valid resume to get recommendations."

    return {
        "detected_skills": detected_skills,
        "top_career_matches": career_scores[:3],
        "recommended_career": top_career,
        "demand": top_data.get("demand", 0),
        "automation_risk": top_data.get("automation_risk", 0),
        "stability": top_data.get("stability", 0),
        "salary": top_data.get("salary", "N/A"),
        "skill_match_percentage": top_skill_info["percentage"],
        "matched_skills": top_skill_info["matched"],
        "missing_skills": top_skill_info["missing"],
        "recommendation": recommendation,
        "resources": top_data.get("resources", []),
    }
