from datetime import datetime
from flask import current_app
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from itsdangerous import URLSafeTimedSerializer as Serializer  # FIX: changed to safe serializer
from app import db, login_manager

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# -------------------- USER --------------------
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    profile = db.relationship('UserProfile', backref='user', uselist=False, cascade="all, delete-orphan")

    def __init__(self, username, email, password, is_admin=False):
        self.username = username
        self.email = email
        self.set_password(password)
        self.is_admin = is_admin
        self.profile = UserProfile()  # Auto create empty profile

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def get_reset_token(self, expires_sec=1800):
        s = Serializer(current_app.config['SECRET_KEY'])
        return s.dumps({'user_id': self.id})

    @staticmethod
    def verify_reset_token(token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            user_id = s.loads(token, max_age=1800)['user_id']
        except Exception:
            return None
        return User.query.get(user_id)

# -------------------- PROFILE --------------------
class UserProfile(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    bio = db.Column(db.Text, nullable=True)
    location = db.Column(db.String(100), nullable=True)
    phone = db.Column(db.String(20), nullable=True)
    website = db.Column(db.String(100), nullable=True)
    avatar = db.Column(db.String(120), nullable=True, default='default.jpg')
    linkedin = db.Column(db.String(100), nullable=True)
    github = db.Column(db.String(100), nullable=True)
    twitter = db.Column(db.String(100), nullable=True)

# -------------------- EDUCATION --------------------
class Education(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    degree = db.Column(db.String(100), nullable=False)
    institution = db.Column(db.String(100), nullable=False)
    graduation_date = db.Column(db.String(50), nullable=False)
    gpa = db.Column(db.String(10), nullable=True)
    achievements = db.Column(db.Text, nullable=True)
    is_default = db.Column(db.Boolean, default=False)

# -------------------- WORK EXPERIENCE --------------------
class WorkExperience(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    company = db.Column(db.String(100), nullable=False)
    location = db.Column(db.String(100), nullable=True)
    start_date = db.Column(db.String(50), nullable=False)
    end_date = db.Column(db.String(50), nullable=True)
    description = db.Column(db.Text, nullable=True)
    skills = db.Column(db.Text, nullable=True)
    is_default = db.Column(db.Boolean, default=False)

# -------------------- PROJECT --------------------
class Project(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    image = db.Column(db.String(120), nullable=True)
    link = db.Column(db.String(200), nullable=True)
    is_default = db.Column(db.Boolean, default=False)

# -------------------- CERTIFICATION --------------------
class Certification(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    organization = db.Column(db.String(100), nullable=True)
    date = db.Column(db.String(50), nullable=True)
    description = db.Column(db.Text, nullable=True)
    is_default = db.Column(db.Boolean, default=False)

# -------------------- SKILL --------------------
class Skill(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    category = db.Column(db.String(100), nullable=False)
    items = db.Column(db.Text, nullable=False)
    is_default = db.Column(db.Boolean, default=False)

# -------------------- MESSAGE --------------------
class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    message = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    is_read = db.Column(db.Boolean, default=False)

# -------------------- DATA SEEDING --------------------
def initialize_default_data():
    if Education.query.filter_by(is_default=True).first() is not None:
        return

    educations = [
        Education(degree="MSc Computer Science", institution="Long Island University", graduation_date="May 2025", gpa="3.8", achievements="Thesis: Sentiment Analysis in Healthcare", is_default=True),
        Education(degree="Bachelor's in Electronics and Communication", institution="Anna University", graduation_date="May 2018", gpa="3.0", achievements="Paper Published: 5G Communications", is_default=True)
    ]
    experiences = [
        WorkExperience(title="Senior Software Engineer (SOX Auditor)", company="Accenture", location="Bengaluru, India (Hybrid)", start_date="Jan 2022", end_date="Jan 2024", description="Managed a sub-project independently...", skills="Mentoring, Project Management", is_default=True),
        WorkExperience(title="Software Engineer (HIPAA Auditor)", company="Accenture", location="Bengaluru, India", start_date="Jul 2020", end_date="Jan 2022", description="Specialized in IT audits...", skills="Tableau, Compliance", is_default=True),
        WorkExperience(title="Associate Software Engineer (Internal Auditor)", company="Accenture", location="Chennai, India", start_date="Sep 2018", end_date="Jun 2020", description="Focused on internal audits...", skills="Auditing, Documentation", is_default=True)
    ]
    projects = [
        Project(title="Advanced E-Health Monitoring Systems", description="A pulse oximeter using Arduino Uno and MAX30102 sensor", is_default=True),
        Project(title="Auto Night Light Using LDR", description="Switches on light based on LDR threshold", is_default=True),
        Project(title="Target Detection Using MATLAB", description="Uses edge detection and template matching", is_default=True)
    ]
    certifications = [
        Certification(name="Microsoft Azure Fundamentals AZ-900", organization="Microsoft", description="Foundational Azure cloud cert", is_default=True),
        Certification(name="Entrepreneurship", organization="IIM Rohtak", description="Covers entrepreneurship and innovation", is_default=True)
    ]
    skills = [
        Skill(category="Programming Languages", items="JavaScript, Java, C#, Python", is_default=True),
        Skill(category="Frontend Development", items="React.js, HTML5, CSS3, Bootstrap", is_default=True),
        Skill(category="Backend Development", items="Node.js, Express.js, Spring Boot", is_default=True),
        Skill(category="API Testing & Automation", items="Postman, Pytest, Selenium", is_default=True),
        Skill(category="Cloud & DevOps", items="AWS (EC2, S3), Jenkins, Azure DevOps", is_default=True),
        Skill(category="Security", items="JWT, OAuth 2.0", is_default=True),
        Skill(category="Test Frameworks", items="POM, Hybrid, Keyword-Driven", is_default=True),
        Skill(category="Defect Management", items="JIRA, Azure, Zephyr", is_default=True)
    ]

    db.session.add_all(educations + experiences + projects + certifications + skills)
    db.session.commit()
