from functools import wraps
from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from app import db
from app.models import User, Campaign, AdRequest
from app.forms import ApproveSponsorForm, FlagForm

admin_bp = Blueprint('admin', __name__)

# Ensure that only the admin has access to these routes
def admin_required(func):
    @wraps(func)
    @login_required
    def wrapper(*args, **kwargs):
        if current_user.role != 'admin':
            flash('Admin access required', 'danger')
            return redirect(url_for('main.index'))
        return func(*args, **kwargs)
    return wrapper

@admin_bp.route('/dashboard')
@admin_required
def dashboard():
    users = User.query.all()
    campaigns = Campaign.query.all()
    ad_requests = AdRequest.query.all()
    flagged_users = User.query.filter_by(flagged=True).all()
    flagged_campaigns = Campaign.query.filter_by(flagged=True).all()
    return render_template('admin/dashboard.html', users=users, campaigns=campaigns, 
                           ad_requests=ad_requests, flagged_users=flagged_users, 
                           flagged_campaigns=flagged_campaigns)

@admin_bp.route('/approve_sponsor', methods=['GET', 'POST'])
@admin_required
def approve_sponsor():
    form = ApproveSponsorForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user:
            user.approved = True
            db.session.commit()
            flash('Sponsor approved', 'success')
        else:
            flash('User not found', 'danger')
        return redirect(url_for('admin.dashboard'))
    return render_template('admin/approve_sponsor.html', form=form)

@admin_bp.route('/flag_user/<int:user_id>', methods=['POST'])
@admin_required
def flag_user(user_id):
    form = FlagForm()
    user = User.query.get_or_404(user_id)
    user.flagged = True
    db.session.commit()
    flash('User flagged', 'success')
    return redirect(url_for('admin.dashboard'))

@admin_bp.route('/flag_campaign/<int:campaign_id>', methods=['POST'])
@admin_required
def flag_campaign(campaign_id):
    form = FlagForm()
    campaign = Campaign.query.get_or_404(campaign_id)
    campaign.flagged = True
    db.session.commit()
    flash('Campaign flagged', 'success')
    return redirect(url_for('admin.dashboard'))
