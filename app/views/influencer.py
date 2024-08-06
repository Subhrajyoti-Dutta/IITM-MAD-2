from functools import wraps
from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from app import db
from app.models import *

influencer_bp = Blueprint('influencer', __name__)

def influencer_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        print(current_user.is_authenticated)
        if current_user.__class__ != Influencer:
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated_function

@influencer_bp.route('/dashboard')
@login_required
@influencer_required
def dashboard():
    return render_template('influencer/dashboard.html')

@influencer_bp.route('/profile')
@login_required
@influencer_required
def profile():
    return render_template('influencer/profile.html')

@influencer_bp.route('/sponsors')
@login_required
@influencer_required
def sponsors():
    return render_template('influencer/sponsors.html')

@influencer_bp.route('/find_campaign')
@login_required
@influencer_required
def find_campaign():
    return render_template('influencer/find_campaign.html')

@influencer_bp.route('/stats')
@login_required
@influencer_required
def stats():
    return render_template('influencer/stats.html')
