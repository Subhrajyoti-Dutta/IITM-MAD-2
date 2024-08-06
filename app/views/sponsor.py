from functools import wraps
from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from app import db
from app.models import Campaign, AdRequest, Sponsor

sponsor_bp = Blueprint('sponsor', __name__)

def sponsor_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if current_user.__class__ != Sponsor:
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated_function

@sponsor_bp.route('/dashboard', methods=['GET'])
@login_required
@sponsor_required
def dashboard():
    return render_template('sponsor/dashboard.html')

@sponsor_bp.route('/profile', methods=['GET', 'POST'])
@login_required
@sponsor_required
def profile():
    return render_template('sponsor/profile.html')

@sponsor_bp.route('/campaigns', methods=['GET', 'POST'])
@login_required
@sponsor_required
def campaigns():
    return render_template('sponsor/campaigns.html')

@sponsor_bp.route('/influencers', methods=['GET', 'POST'])
@login_required
@sponsor_required
def influencers():
    return render_template('sponsor/influencers.html')

@sponsor_bp.route('/stats', methods=['GET', 'POST'])
@login_required
@sponsor_required
def stats():
    return render_template('sponsor/stats.html')
