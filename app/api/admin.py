from flask import Blueprint, request, jsonify
from flask_restful import Resource, Api
from flask_login import login_required, current_user
from app.models import db, Sponsor, Influencer, Campaign, Admin, AdRequest

admin_api_bp = Blueprint('admin_api', __name__)
api = Api(admin_api_bp)

# def admin_required(f):
#     @wraps(f)
#     def decorated_function(*args, **kwargs):
#         if current_user.__class__ != Admin:
#             return jsonify({"message": "Admin access required"}), 403
#         return f(*args, **kwargs)
#     return decorated_function

class SponsorsAPI(Resource):
    def get(self):
        sponsors = Sponsor.query.all()
        return jsonify([sponsor._to_dict() for sponsor in sponsors])

    def put(self, sponsor_id):
        sponsor = Sponsor.query.get_or_404(sponsor_id)
        data = request.get_json()
        if 'Flag' in data:
            sponsor.flag = data['Flag']
        db.session.commit()
        return jsonify(sponsor._to_dict())

class InfluencersAPI(Resource):
    def get(self):
        influencers = Influencer.query.all()
        return jsonify([influencer._to_dict() for influencer in influencers])

    def put(self, influencer_id):
        influencer = Influencer.query.get_or_404(influencer_id)
        data = request.get_json()
        if 'Flag' in data:
            influencer.flag = data['Flag']
        db.session.commit()
        return jsonify(influencer._to_dict())



class CampaignsAPI(Resource):
    def get(self):
        campaigns = Campaign.query.all()
        ad_requests = list()
        for campaign in campaigns:
            ad = campaign._to_dict()
            ad["Ads"] = [ad._to_dict() for ad in AdRequest.query.filter_by(campaign_id = campaign.campaign_id).all()]
            ad_requests.append(ad)
        print(ad_requests[0])
        return jsonify(ad_requests)

    def put(self, campaign_id):
        campaign = Campaign.query.get_or_404(campaign_id)
        data = request.get_json()
        if 'Flag' in data:
            campaign.flag = data['Flag']
        db.session.commit()
        return jsonify(campaign._to_dict())

class AdsAPI(Resource):
    
    def get(self, campaign_id):
        ad_requests = AdRequest.query.filter_by(campaign_id=campaign_id).all()
        return jsonify([ad_request._to_dict() for ad_request in ad_requests])

    def put(self, campaign_id, ad_id):
        ad_request = AdRequest.query.filter_by(campaign_id=campaign_id, ad_id=ad_id).first()
        data = request.get_json()
        if 'Flag' in data:
            ad_request.flag = data['Flag']
        db.session.commit()
        return jsonify(ad_request._to_dict())


class AdminsAPI(Resource):
    def get(self, admin_id=None):
        if admin_id is None:
            admins = Admin.query.all()
            return jsonify([admin.to_dict() for admin in admins])
        else:
            admin = Admin.query.get(admin_id)
            return admin.to_dict()

    def put(self, admin_id):
        admin = Admin.query.get_or_404(admin_id)
        data = request.get_json()
        if 'Flag' in data:
            admin.flag = data['Flag']
        db.session.commit()
        return jsonify(admin.to_dict())

    def post(self):
        data = request.get_json()
        new_admin = Admin(
            username=data['Username'],
            password=data['Password'],
            full_name=data.get('Full_Name'),
            email=data.get('Email'),
            position=data['Position'],
        )
        db.session.add(new_admin)
        db.session.commit()
        return jsonify(new_admin.to_dict())

    def delete(self, admin_id):
        admin = Admin.query.get_or_404(admin_id)
        db.session.delete(admin)
        db.session.commit()
        return '', 204


class StatisticsAPI(Resource):
    def get(self):
        total_influencers = Influencer.query.count()
        flagged_influencers = Influencer.query.filter_by(flag=True).count()
        total_sponsors = Sponsor.query.count()
        flagged_sponsors = Sponsor.query.filter_by(flag=True).count()
        total_campaigns = Campaign.query.count()
        flagged_campaigns = Campaign.query.filter_by(flag=True).count()
        flagged_ads = AdRequest.query.filter_by(flag=True).count()

        return {
            "totalInfluencers": total_influencers,
            "flaggedInfluencers": flagged_influencers,
            "totalSponsors": total_sponsors,
            "flaggedSponsors": flagged_sponsors,
            "totalCampaigns": total_campaigns,
            "flaggedCampaigns": flagged_campaigns,
            "flaggedAds": flagged_ads,
        }