from flask import Blueprint, render_template, redirect, url_for, flash, request, jsonify
from flask_login import login_user, logout_user, login_required, current_user
from app.models import *
from app import db
import random

auth_bp = Blueprint('auth', __name__)
@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        if current_user.is_authenticated:
            if current_user.role == 'influencer':
                return redirect(url_for('influencer.influencer_dashboard'))
            elif current_user.role == 'sponsor':
                return redirect(url_for('sponsor.dashboard'))
            elif current_user.role == 'admin':
                return redirect(url_for('admin.dashboard'))
        return render_template('auth/login.html')

    if request.method == 'POST':
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')
        remember = data.get('remember', False)

        user = User.query.filter_by(username=username).first()

        if user and user.password == password:
            login_user(user, remember=remember)
            if user.role == 'influencer':
                return jsonify(success=True, next=url_for('influencer.influencer_dashboard'))
            elif user.role == 'sponsor':
                return jsonify(success=True, next=url_for('sponsor.dashboard'))
            elif user.role == 'admin':
                return jsonify(success=True, next=url_for('admin.dashboard'))
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
    if request.method == 'POST':
        if request.is_json:
            print("Log 1")
            data = request.get_json()
            username = data.get('username')
            password = data.get('password')
            full_name = data.get('full_name')
            country_code = data.get('country_code')
            phone = data.get('phone')
            youtube = data.get('youtube', False)
            twitter = data.get('twitter', False)
            instagram = data.get('instagram', False)
            others = data.get('others', False)
            print("Log 2")

            # Generate a unique ID using numpy random.randint with dtype=np.int64
            while True:
                new_id = random.randint(1, 2**31 - 1)
                if not User.query.get(new_id):
                    break

            # Create a new User instance
            new_user = User(id=new_id, username=username, password=password, role='influencer')
            
            print("Log 3")
            # Create a new Influencer instance
            new_influencer = Influencer(
                id=new_user.id,
                full_name=full_name,
                country_code=country_code,
                phone=phone,
                youtube=youtube,
                twitter=twitter,
                instagram=instagram,
                others=others
            )
            
            # Add the new user and influencer to the session and commit
            print("Log 4")
            db.session.add(new_user)
            print(dir(new_user))
            print("Hello")
            db.session.commit()
            print("Hello2")
            db.session.add(new_influencer)
            print("Hello3")
            db.session.commit()
            print("Hello4")

            return jsonify(success=True, message='Registration successful', next=url_for('auth.login'))
        else:
            return jsonify(success=False, message='Request must be JSON'), 415
    
    return render_template('auth/register_influencer.html')
