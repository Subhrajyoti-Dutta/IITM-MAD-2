from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from app import db
from app.models import Campaign, AdRequest, Sponsor

sponsor_bp = Blueprint('sponsor', __name__)

@sponsor_bp.route('/dashboard', methods=['GET'])
@login_required
def dashboard():
    if current_user.__class__ != Sponsor:
        return redirect(url_for('auth.logout'))

    return render_template('sponsor/dashboard.html')

@sponsor_bp.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    if current_user.__class__ != Sponsor:
        return redirect(url_for('auth.logout'))

    return render_template('sponsor/profile.html')

@sponsor_bp.route('/campaigns', methods=['GET', 'POST'])
@login_required
def campaigns():
    if current_user.__class__ != Sponsor:
        return redirect(url_for('auth.logout'))

    return render_template('sponsor/campaigns.html')

@sponsor_bp.route('/influencers', methods=['GET', 'POST'])
@login_required
def influencers():
    if current_user.__class__ != Sponsor:
        return redirect(url_for('auth.logout'))

    return render_template('sponsor/influencers.html')

@sponsor_bp.route('/stats', methods=['GET', 'POST'])
@login_required
def stats():
    if current_user.__class__ != Sponsor:
        return redirect(url_for('auth.logout'))

    return render_template('sponsor/stats.html')
