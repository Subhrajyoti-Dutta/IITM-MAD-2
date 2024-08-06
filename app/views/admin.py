from functools import wraps
from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from app import db
from app.models import Campaign, AdRequest, Influencer, Sponsor, Admin

admin_bp = Blueprint('admin', __name__)

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        print(current_user.is_authenticated)
        if current_user.__class__ != Admin:
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated_function

@admin_bp.route('/dashboard')
@login_required
@admin_required
def dashboard():
    print("Hello World")
    return render_template('admin/dashboard.html')

@admin_bp.route('/influencers')
@login_required
@admin_required
def influencers():
    influencers = Influencer.query.all()
    return render_template('admin/influencers.html', influencers=influencers)

@admin_bp.route('/sponsors')
@login_required
@admin_required
def sponsors():
    sponsors = Sponsor.query.all()
    return render_template('admin/sponsors.html', sponsors=sponsors)

@admin_bp.route('/campaigns')
@login_required
@admin_required
def campaigns():
    campaigns = Campaign.query.all()
    return render_template('admin/campaigns.html', campaigns=campaigns)

@admin_bp.route('/admins')
@login_required
@admin_required
def admins():
    admins = Admin.query.all()
    return render_template('admin/admins.html', admins=admins)
