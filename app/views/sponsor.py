from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from app import db
from app.models import Campaign, AdRequest, User
from app.forms import CampaignForm, AdRequestFormSponsor, SearchForm

sponsor_bp = Blueprint('sponsor', __name__)

@sponsor_bp.route('/dashboard')
@login_required
def dashboard():
    if current_user.role != 'sponsor':
        flash('Sponsor access required', 'danger')
        return redirect(url_for('main.index'))
    
    campaigns = Campaign.query.filter_by(sponsor_id=current_user.id).all()
    return render_template('sponsor/dashboard.html', campaigns=campaigns)

@sponsor_bp.route('/campaign/new', methods=['GET', 'POST'])
@login_required
def new_campaign():
    if current_user.role != 'sponsor':
        flash('Sponsor access required', 'danger')
        return redirect(url_for('main.index'))

    form = CampaignForm()
    if form.validate_on_submit():
        campaign = Campaign(
            name=form.name.data,
            description=form.description.data,
            start_date=form.start_date.data,
            end_date=form.end_date.data,
            budget=form.budget.data,
            visibility=form.visibility.data,
            goals=form.goals.data,
            sponsor_id=current_user.id
        )
        db.session.add(campaign)
        db.session.commit()
        flash('Campaign created successfully', 'success')
        return redirect(url_for('sponsor.dashboard'))
    return render_template('sponsor/new_campaign.html', form=form)

@sponsor_bp.route('/campaign/<int:campaign_id>/update', methods=['GET', 'POST'])
@login_required
def update_campaign(campaign_id):
    if current_user.role != 'sponsor':
        flash('Sponsor access required', 'danger')
        return redirect(url_for('main.index'))

    campaign = Campaign.query.get_or_404(campaign_id)
    if campaign.sponsor_id != current_user.id:
        flash('Unauthorized action', 'danger')
        return redirect(url_for('sponsor.dashboard'))

    form = CampaignForm(obj=campaign)
    if form.validate_on_submit():
        campaign.name = form.name.data
        campaign.description = form.description.data
        campaign.start_date = form.start_date.data
        campaign.end_date = form.end_date.data
        campaign.budget = form.budget.data
        campaign.visibility = form.visibility.data
        campaign.goals = form.goals.data
        db.session.commit()
        flash('Campaign updated successfully', 'success')
        return redirect(url_for('sponsor.dashboard'))
    return render_template('sponsor/update_campaign.html', form=form, campaign=campaign)

@sponsor_bp.route('/campaign/<int:campaign_id>/delete', methods=['POST'])
@login_required
def delete_campaign(campaign_id):
    if current_user.role != 'sponsor':
        flash('Sponsor access required', 'danger')
        return redirect(url_for('main.index'))

    campaign = Campaign.query.get_or_404(campaign_id)
    if campaign.sponsor_id != current_user.id:
        flash('Unauthorized action', 'danger')
        return redirect(url_for('sponsor.dashboard'))

    db.session.delete(campaign)
    db.session.commit()
    flash('Campaign deleted successfully', 'success')
    return redirect(url_for('sponsor.dashboard'))

@sponsor_bp.route('/ad_request/new/<int:campaign_id>', methods=['GET', 'POST'])
@login_required
def new_ad_request(campaign_id):
    if current_user.role != 'sponsor':
        flash('Sponsor access required', 'danger')
        return redirect(url_for('main.index'))

    campaign = Campaign.query.get_or_404(campaign_id)
    if campaign.sponsor_id != current_user.id:
        flash('Unauthorized action', 'danger')
        return redirect(url_for('sponsor.dashboard'))

    form = AdRequestFormSponsor()
    if form.validate_on_submit():
        ad_request = AdRequest(
            campaign_id=campaign.id,
            influencer_id=form.influencer_id.data,
            messages=form.messages.data,
            requirements=form.requirements.data,
            payment_amount=form.payment_amount.data,
            status='Pending'
        )
        db.session.add(ad_request)
        db.session.commit()
        flash('Ad request created successfully', 'success')
        return redirect(url_for('sponsor.dashboard'))
    return render_template('sponsor/new_ad_request.html', form=form, campaign=campaign)

@sponsor_bp.route('/search_influencers', methods=['GET', 'POST'])
@login_required
def search_influencers():
    if current_user.role != 'sponsor':
        flash('Sponsor access required', 'danger')
        return redirect(url_for('main.index'))

    form = SearchForm()
    influencers = []
    if form.validate_on_submit():
        search_term = form.search_term.data
        influencers = User.query.filter(User.username.contains(search_term), User.role == 'influencer').all()
    return render_template('sponsor/search_influencers.html', form=form, influencers=influencers)
