from flask import Blueprint, render_template, url_for, flash, redirect, request
from flask_login import login_user, current_user, logout_user, login_required
from app import db, mail
from app.models import User, UserProfile
from app.forms import (
    RegistrationForm, LoginForm, RequestResetForm,
    ResetPasswordForm, UpdateProfileForm
)
from flask_mail import Message
from werkzeug.utils import secure_filename
import os

auth = Blueprint('auth', __name__)

# Utility: Save uploaded picture
def save_picture(file):
    filename = secure_filename(file.filename)
    file_path = os.path.join('app', 'static', 'uploads', filename)
    file.save(file_path)
    return filename

# -------------------- Register --------------------
@auth.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, 
                    email=form.email.data, 
                    password=form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created! You can now log in.', 'success')
        return redirect(url_for('auth.login'))
    
    return render_template('auth/register.html', title='Register', form=form)

# -------------------- Login --------------------
@auth.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('portfolio.dashboard'))
    
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('portfolio.dashboard'))
        else:
            flash('Login unsuccessful. Please check email and password.', 'danger')
    
    return render_template('auth/login.html', title='Login', form=form)

# -------------------- Logout --------------------
@auth.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('main.index'))

# -------------------- Profile --------------------
@auth.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    form = UpdateProfileForm(obj=current_user)

    if form.validate_on_submit():
        # Update User basic info
        current_user.username = form.username.data
        current_user.email = form.email.data

        # Create profile if not existing
        if not current_user.profile:
            current_user.profile = UserProfile()

        current_user.profile.bio = form.bio.data
        current_user.profile.location = form.location.data
        current_user.profile.phone = form.phone.data
        current_user.profile.website = form.website.data
        current_user.profile.linkedin = form.linkedin.data
        current_user.profile.github = form.github.data
        current_user.profile.twitter = form.twitter.data

        if form.avatar.data:
            picture_filename = save_picture(form.avatar.data)
            current_user.profile.avatar = picture_filename

        db.session.commit()
        flash('Your profile has been updated!', 'success')
        return redirect(url_for('auth.profile'))

    # Pre-populate form for GET
    if request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email

        if current_user.profile:
            form.bio.data = current_user.profile.bio
            form.location.data = current_user.profile.location
            form.phone.data = current_user.profile.phone
            form.website.data = current_user.profile.website
            form.linkedin.data = current_user.profile.linkedin
            form.github.data = current_user.profile.github
            form.twitter.data = current_user.profile.twitter

    return render_template('auth/profile.html', title='Profile', form=form)

# -------------------- Send Reset Email --------------------
def send_reset_email(user):
    token = user.get_reset_token()
    msg = Message('Password Reset Request', recipients=[user.email])
    msg.body = f'''To reset your password, visit the following link:
{url_for('auth.reset_token', token=token, _external=True)}

If you did not make this request, simply ignore this email and no changes will be made.
'''
    mail.send(msg)

# -------------------- Request Reset --------------------
@auth.route('/reset_password', methods=['GET', 'POST'])
def reset_request():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    
    form = RequestResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            send_reset_email(user)
            flash('An email has been sent with instructions to reset your password.', 'info')
        else:
            flash('No account found with that email.', 'danger')
        return redirect(url_for('auth.login'))
    
    return render_template('auth/reset_request.html', title='Reset Password', form=form)

# -------------------- Token-based Reset --------------------
@auth.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_token(token):
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))

    user = User.verify_reset_token(token)
    if user is None:
        flash('That is an invalid or expired token', 'warning')
        return redirect(url_for('auth.reset_request'))
    
    form = ResetPasswordForm()
    if form.validate_on_submit():
        user.set_password(form.password.data)
        db.session.commit()
        flash('Your password has been updated! You are now able to log in.', 'success')
        return redirect(url_for('auth.login'))
    
    return render_template('auth/reset_token.html', title='Reset Password', form=form)
