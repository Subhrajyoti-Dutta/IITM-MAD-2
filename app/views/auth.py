from flask import Blueprint, render_template, redirect, url_for, flash, request, jsonify
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from app import db
from app.models import User

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        if current_user.is_authenticated:
            if current_user.role == 'Influencer':
                return redirect(url_for('influencer.dashboard'))
            elif current_user.role == 'Sponsor':
                return redirect(url_for('sponsor.dashboard'))
            return redirect(url_for('main.index'))
        return render_template('auth/login.html')

    if request.method == 'POST':
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')
        remember = data.get('remember', False)

        user = User.query.filter_by(username=username).first()

        if user and check_password_hash(user.password, password):
            login_user(user, remember=remember)
            if user.role == 'Influencer':
                return jsonify(success=True, next=url_for('influencer.dashboard'))
            elif user.role == 'Sponsor':
                return jsonify(success=True, next=url_for('sponsor.dashboard'))
            else:
                return jsonify(success=True, next=url_for('main.index'))
        return jsonify(success=False, message='Invalid username or password')

@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))

@auth_bp.route('/register_sponsor', methods=['GET', 'POST'])
def register_sponsor():
    if request.method == 'GET':
        return render_template('auth/register_sponsor.html')
    
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        company_name = request.form.get('company_name')
        industry = request.form.get('industry')
        hashed_password = generate_password_hash(password, method='sha256')
        user = User(username=username, password=hashed_password, role='Sponsor')
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created! You can now log in', 'success')
        return redirect(url_for('auth.login'))

@auth_bp.route('/register_influencer', methods=['GET', 'POST'])
def register_influencer():
    if request.method == 'GET':
        return render_template('auth/register_influencer.html')
    
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        niche = request.form.get('niche')
        reach = request.form.get('reach')
        hashed_password = generate_password_hash(password, method='sha256')
        user = User(username=username, password=hashed_password, role='Influencer')
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created! You can now log in', 'success')
        return redirect(url_for('auth.login'))
