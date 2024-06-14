from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from app import db
from app.models import AdRequest, Campaign, User
from app.forms import AdRequestFormInfluencer, UpdateProfileForm, SearchForm

influencer_bp = Blueprint('influencer', __name__)

@influencer_bp.route('/dashboard')
@login_required
def dashboard():
    if current_user.role != 'influencer':
        flash('Influencer access required', 'danger')
        return redirect(url_for('main.index'))
    
    ad_requests = AdRequest.query.filter_by(influencer_id=current_user.id).all()
    return render_template('influencer/dashboard.html', ad_requests=ad_requests)

@influencer_bp.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    if current_user.role != 'influencer':
        flash('Influencer access required', 'danger')
        return redirect(url_for('main.index'))
    
    form = UpdateProfileForm(obj=current_user)
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.category = form.category.data
        current_user.niche = form.niche.data
        current_user.reach = form.reach.data
        db.session.commit()
        flash('Profile updated successfully', 'success')
        return redirect(url_for('influencer.profile'))
    return render_template('influencer/profile.html', form=form)

@influencer_bp.route('/ad_requests')
@login_required
def ad_requests():
    if current_user.role != 'influencer':
        flash('Influencer access required', 'danger')
        return redirect(url_for('main.index'))
    
    ad_requests = AdRequest.query.filter_by(influencer_id=current_user.id).all()
    return render_template('influencer/ad_requests.html', ad_requests=ad_requests)

@influencer_bp.route('/ad_request/<int:ad_request_id>/respond', methods=['GET', 'POST'])
@login_required
def respond_ad_request(ad_request_id):
    if current_user.role != 'influencer':
        flash('Influencer access required', 'danger')
        return redirect(url_for('main.index'))
    
    ad_request = AdRequest.query.get_or_404(ad_request_id)
    if ad_request.influencer_id != current_user.id:
        flash('Unauthorized action', 'danger')
        return redirect(url_for('influencer.dashboard'))

    form = AdRequestFormInfluencer(obj=ad_request)
    if form.validate_on_submit():
        ad_request.sponsor_id = form.sponsor_id.data
        ad_request.messages = form.messages.data
        ad_request.requirements = form.requirements.data
        ad_request.payment_amount = form.payment_amount.data
        ad_request.status = form.status.data
        db.session.commit()
        flash('Ad request updated successfully', 'success')
        return redirect(url_for('influencer.ad_requests'))
    return render_template('influencer/respond_ad_request.html', form=form, ad_request=ad_request)

@influencer_bp.route('/search_campaigns', methods=['GET', 'POST'])
@login_required
def search_campaigns():
    if current_user.role != 'influencer':
        flash('Influencer access required', 'danger')
        return redirect(url_for('main.index'))
    
    form = SearchForm()
    campaigns = []
    if form.validate_on_submit():
        search_term = form.search_term.data
        campaigns = Campaign.query.filter(Campaign.name.contains(search_term), Campaign.visibility == 'public').all()
    return render_template('influencer/search_campaigns.html', form=form, campaigns=campaigns)
