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

    from app.api.influencer import InfluencerListAPI, InfluencerAPI
    from app.api.sponsor import SponsorAPI, SponsorListAPI

    api = Api(app)
    api.add_resource(InfluencerListAPI, '/api/influencer_api/influencers')
    api.add_resource(InfluencerAPI, '/api/influencer_api/influencer/<int:influencer_id>')
    api.add_resource(SponsorListAPI, '/api/sponsor_api/sponsors')
    api.add_resource(SponsorAPI,'/api/sponsor_api/sponsor/<int:sponsor_id>')
    
    return app

# User loader callback
@login_manager.user_loader
def load_user(user_id):
    from app.models import User
    return User.query.get(int(user_id))

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
