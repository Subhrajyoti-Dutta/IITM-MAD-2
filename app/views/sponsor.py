from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from app import db
from app.models import Campaign, AdRequest
from app.forms import CampaignForm, AdRequestFormSponsor, SearchForm

sponsor_bp = Blueprint('sponsor', __name__)
