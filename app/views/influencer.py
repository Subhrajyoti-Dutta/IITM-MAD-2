from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from app import db
from app.models import *

influencer_bp = Blueprint('influencer', __name__)

@influencer_bp.route('/dashboard')
@login_required
def dashboard():
    if current_user.__class__ != Influencer:
        return redirect(url_for('auth.logout'))
    
    return render_template('influencer/dashboard.html')

@influencer_bp.route('/profile')
@login_required
def profile():
    if current_user.__class__ != Influencer:
        return redirect(url_for('auth.logout'))

    return render_template('influencer/profile.html')

@influencer_bp.route('/sponsors')
@login_required
def sponsors():
    if current_user.__class__ != Influencer:
        return redirect(url_for('auth.logout'))

    return render_template('influencer/sponsors.html')

@influencer_bp.route('/find_campaign')
@login_required
def find_campaign():
    if current_user.__class__ != Influencer:
        return redirect(url_for('auth.logout'))

    return render_template('influencer/find_campaign.html')

@influencer_bp.route('/stats')
@login_required
def stats():
    if current_user.__class__ != Influencer:
        return redirect(url_for('auth.logout'))

    return render_template('influencer/stats.html')
