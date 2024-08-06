from flask import Flask
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bootstrap import Bootstrap
from redis import Redis
from celery import Celery
from flask_migrate import Migrate

# Initialize extensions
db = SQLAlchemy()
login_manager = LoginManager()
bootstrap = Bootstrap()
celery = Celery(__name__, broker='redis://localhost:6379/0')
migrate = Migrate()

def create_app():
    app = Flask(__name__)
    app.config.from_object('app.config.Config')

    # Initialize extensions
    db.init_app(app)
    login_manager.init_app(app)
    bootstrap.init_app(app)
    migrate.init_app(app, db)

    # Set up the login manager
    login_manager.login_view = 'auth.login'
    login_manager.login_message_category = 'info'

    # Register blueprints
    from app.views.auth import auth_bp
    from app.views.admin import admin_bp
    from app.views.sponsor import sponsor_bp
    from app.views.influencer import influencer_bp
    from app.views import main_bp

    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(admin_bp, url_prefix='/admin')
    app.register_blueprint(sponsor_bp, url_prefix='/sponsor')
    app.register_blueprint(influencer_bp, url_prefix='/influencer')
    app.register_blueprint(main_bp)

    from app.api.influencer import InfluencerListAPI, InfluencerAPI, InfluAdAPI
    from app.api.sponsor import SponsorAPI, SponsorListAPI, SponAdAPI
    from app.api.campaign import CampaignAPI, CampaignListAPI
    from app.api.adrequest import AdRequestAPI, AdRequestListAPI
    from app.api.adperformance import AdPerformanceAPI
    from app.api.admin import SponsorsAPI, InfluencersAPI, CampaignsAPI, AdminsAPI, AdsAPI, StatisticsAPI

    api = Api(app)
    api.add_resource(InfluencerListAPI,     '/api/influencer_api/influencers')
    api.add_resource(InfluencerAPI,         '/api/influencer_api/influencer', '/api/influencer_api/influencer/<int:influencer_id>')
    api.add_resource(InfluAdAPI,            '/api/influencer_api/influencer/<int:influencer_id>/campaign/<status>', '/api/influencer_api/influencer/<int:influencer_id>/campaigns')
    api.add_resource(SponsorListAPI,        '/api/sponsor_api/sponsors')
    api.add_resource(SponsorAPI,            '/api/sponsor_api/sponsor', '/api/sponsor_api/sponsor/<int:sponsor_id>')
    api.add_resource(SponAdAPI,             '/api/sponsor_api/sponsor/<int:sponsor_id>/campaign/<status>', '/api/sponsor_api/sponsor/<int:sponsor_id>/campaigns')
    api.add_resource(CampaignAPI,           '/api/campaign_api/campaign/<int:campaign_id>', '/api/campaign_api/campaign')
    api.add_resource(CampaignListAPI,       '/api/campaign_api/campaigns')
    api.add_resource(AdRequestAPI,          '/api/campaign_api/campaign/<int:campaign_id>/adrequest/<int:ad_id>', '/api/campaign_api/campaign/<int:campaign_id>/adrequest')
    api.add_resource(AdRequestListAPI,      '/api/campaign_api/campaign/<int:campaign_id>/adrequests')
    api.add_resource(AdPerformanceAPI,      '/api/campaign_api/campaign/<int:campaign_id>/adrequest/<int:ad_id>/performance')
    api.add_resource(SponsorsAPI,           '/api/admin_api/sponsors', '/api/admin_api/sponsor/<int:sponsor_id>')
    api.add_resource(InfluencersAPI,        '/api/admin_api/influencers', '/api/admin_api/influencer/<int:influencer_id>')
    api.add_resource(CampaignsAPI,          '/api/admin_api/campaigns', '/api/admin_api/campaign/<int:campaign_id>')
    api.add_resource(AdsAPI,                '/api/admin_api/campaign/<int:campaign_id>/ads', '/api/admin_api/campaign/<int:campaign_id>/ad/<int:ad_id>')
    api.add_resource(AdminsAPI,             '/api/admin_api/admins', '/api/admin_api/admin/<int:admin_id>')
    api.add_resource(StatisticsAPI,         '/api/admin_api/statistics')
    return app

# User loader callback
@login_manager.user_loader
def load_user(user_id):
    from app.models import Sponsor, Influencer, Admin
    
    # If not found, attempt to load the user from the Sponsor model
    sponsor = Sponsor.query.get(int(user_id))
    if sponsor:
        return sponsor
    
    # If not found, attempt to load the user from the Influencer model
    influencer = Influencer.query.get(int(user_id))
    if influencer:
        return influencer
    
    admin = Admin.query.get(int(user_id))
    if admin:
        return admin

# Celery configuration
def make_celery(app):
    celery.conf.update(app.config)
    TaskBase = celery.Task

    class ContextTask(TaskBase):
        abstract = True

        def __call__(self, *args, **kwargs):
            with app.app_context():
                return TaskBase.__call__(self, *args, **kwargs)

    celery.Task = ContextTask
    return celery

celery = make_celery(create_app())
