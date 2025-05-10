from flask import Blueprint, render_template, flash, redirect, url_for, request
from flask_login import login_required, current_user
from app import db
from app.models import User, Education, WorkExperience, Project, Certification, Skill

portfolio = Blueprint('portfolio', __name__)

@portfolio.route('/dashboard')
@login_required
def dashboard():
    return render_template('portfolio/dashboard.html', title='Dashboard')

@portfolio.route('/education')
@login_required
def education():
    # Get both default and user-specific education entries
    default_educations = Education.query.filter_by(is_default=True).all()
    # In a real app, you'd get user-specific entries here
    # user_educations = Education.query.filter_by(user_id=current_user.id).all()
    
    return render_template('portfolio/education.html', 
                           title='Education',
                           educations=default_educations)

@portfolio.route('/experience')
@login_required
def experience():
    # Get both default and user-specific experience entries
    default_experiences = WorkExperience.query.filter_by(is_default=True).all()
    
    return render_template('portfolio/experience.html', 
                           title='Work Experience',
                           experiences=default_experiences)

@portfolio.route('/projects')
@login_required
def projects():
    # Get both default and user-specific project entries
    default_projects = Project.query.filter_by(is_default=True).all()
    
    return render_template('portfolio/projects.html', 
                           title='Projects',
                           projects=default_projects)

@portfolio.route('/certifications')
@login_required
def certifications():
    # Get both default and user-specific certification entries
    default_certifications = Certification.query.filter_by(is_default=True).all()
    
    return render_template('portfolio/certifications.html', 
                           title='Certifications',
                           certifications=default_certifications)

@portfolio.route('/skills')
@login_required
def skills():
    # Get both default and user-specific skill entries
    default_skills = Skill.query.filter_by(is_default=True).all()
    
    return render_template('portfolio/skills.html', 
                           title='Skills',
                           skills=default_skills)