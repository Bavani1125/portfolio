from flask import Blueprint, render_template, flash, redirect, url_for
from app import db
from app.models import Education, WorkExperience, Project, Certification, Skill, Message
from app.forms import ContactForm

main = Blueprint('main', __name__)

@main.route('/')
@main.route('/home')
def index():
    educations = Education.query.filter_by(is_default=True).all()
    experiences = WorkExperience.query.filter_by(is_default=True).all()
    projects = Project.query.filter_by(is_default=True).all()
    certifications = Certification.query.filter_by(is_default=True).all()
    skills = Skill.query.filter_by(is_default=True).all()
    
    contact_form = ContactForm()
    
    return render_template('main/index.html', 
                           title='Portfolio', 
                           educations=educations,
                           experiences=experiences,
                           projects=projects,
                           certifications=certifications,
                           skills=skills,
                           form=contact_form)

@main.route('/contact', methods=['GET', 'POST'])
def contact():
    form = ContactForm()
    if form.validate_on_submit():
        message = Message(
            name=form.name.data,
            email=form.email.data,
            message=form.message.data
        )
        db.session.add(message)
        db.session.commit()
        flash('Your message has been sent! Thank you for contacting me.', 'success')
        return redirect(url_for('main.index'))
        
    return render_template('main/contact.html', title='Contact Me', form=form)

@main.route('/about')
def about():
    return render_template('main/about.html', title='About Me')
