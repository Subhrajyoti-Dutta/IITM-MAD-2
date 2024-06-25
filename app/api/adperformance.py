from flask import Blueprint, request, jsonify, abort
from flask_restful import Resource, Api
from app.models import db, AdPerformance, AdRequest, Campaign

ad_performance_bp = Blueprint('ad_performance', __name__)
api = Api(ad_performance_bp)

def abort_if_ad_doesnt_exist(campaign_id, ad_id):
    ad = AdRequest.query.filter_by(campaign_id=campaign_id, ad_id=ad_id).first()
    if not ad:
        abort(404, description = f"AdRequest {ad_id} in Campaign {campaign_id} doesn't exist" )
    return ad

def abort_if_ad_is_not_active(ad_id):
    ad = AdPerformance.query.get(ad_id)
    if not ad:
        abort(404, description=f"AdPerformance {ad_id} isn't active")
    return ad

class AdPerformanceAPI(Resource):
    def get(self, campaign_id, ad_id):
        abort_if_ad_doesnt_exist(campaign_id, ad_id)
        ad_performance = abort_if_ad_is_not_active(ad_id)
        if ad_performance:
            return ad_performance.to_dict()
        else:
            abort(404, description=f"AdPerformance for AdRequest {ad_id} doesn't exist")

    def put(self, campaign_id, ad_id):
        abort_if_ad_doesnt_exist(campaign_id, ad_id)
        ad_performance = abort_if_ad_is_not_active(ad_id)
        data = request.get_json()
        ad_performance.reach = data.get('Reach', ad_performance.reach)
        ad_performance.posts = data.get('Posts', ad_performance.posts)
        ad_performance.likes = data.get('Likes', ad_performance.likes)
        ad_performance.rating = data.get('Rating', ad_performance.rating)
        
        db.session.commit()
        return ad_performance.to_dict(), 201

    def post(self, campaign_id, ad_id):
        ad_status = abort_if_ad_doesnt_exist(campaign_id, ad_id).status
        if ad_status == "Active" and not AdPerformance.query.get(ad_id):
            data = request.get_json()
            ad_performance = AdPerformance(
                ad_id=ad_id,
                reach=data.get('Reach', 0),
                posts=data.get('Posts', 0),
                likes=data.get('Likes', 0),
                rating=data.get('Rating', 0)
            )
            db.session.add(ad_performance)
            db.session.commit()
            return ad_performance.to_dict(), 201
        else:
            return {"message": f"AdRequest {ad_id} isn't active"}, 404

    def delete(self, campaign_id, ad_id):
        abort_if_ad_doesnt_exist(campaign_id, ad_id)
        abort_if_ad_is_not_active(ad_id)
        ad_performance = AdPerformance.query.filter_by(ad_id=ad_id).first()
        db.session.delete(ad_performance)
        db.session.commit()
        return '', 204
