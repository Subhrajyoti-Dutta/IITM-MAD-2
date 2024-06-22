from flask import Blueprint, request, jsonify, abort
from flask_restful import Resource, Api
from app.models import db, AdRequest, Campaign
import random

ad_request_blueprint = Blueprint('ad_requests', __name__)
api = Api(ad_request_blueprint)

def abort_if_campaign_or_ad_doesnt_exist(campaign_id, ad_id=None):
    campaign = Campaign.query.get(campaign_id)
    if not campaign:
        abort(404, message=f"Campaign {campaign_id} doesn't exist")
    if ad_id is not None:
        ad_request = AdRequest.query.filter_by(campaign_id=campaign_id, id=ad_id).first()
        if not ad_request:
            abort(404, message=f"AdRequest {ad_id} in Campaign {campaign_id} doesn't exist")

class AdRequestAPI(Resource):
    def get(self, campaign_id, ad_id):
        abort_if_campaign_or_ad_doesnt_exist(campaign_id, ad_id)
        ad_request = AdRequest.query.filter_by(campaign_id=campaign_id, id=ad_id).first_or_404()
        return jsonify(ad_request.to_dict())

    def put(self, campaign_id, ad_id):
        abort_if_campaign_or_ad_doesnt_exist(campaign_id, ad_id)
        ad_request = AdRequest.query.filter_by(campaign_id=campaign_id, id=ad_id).first_or_404()
        data = request.get_json()

        ad_request.influencer_id = data.get('influencer_id', ad_request.influencer_id)
        ad_request.messages = data.get('messages', ad_request.messages)
        ad_request.requirements = data.get('requirements', ad_request.requirements)
        ad_request.payment_amount = data.get('payment_amount', ad_request.payment_amount)
        ad_request.status = data.get('status', ad_request.status)

        db.session.commit()
        return jsonify(ad_request.to_dict())

    def post(self, campaign_id):
        abort_if_campaign_or_ad_doesnt_exist(campaign_id)
        data = request.get_json()
        while True:
            new_id = random.randint(1, 2**31 - 1)
            if not Campaign.query.get(new_id):
                break
        new_ad_request = AdRequest(
            id = new_id,
            campaign_id=campaign_id,
            influencer_id=data.get('influencer_id'),
            messages=data.get('messages'),
            requirements=data.get('requirements'),
            payment_amount=data.get('payment_amount'),
            status=data.get('status')
        )
        db.session.add(new_ad_request)
        db.session.commit()
        return jsonify(new_ad_request.to_dict()), 201

    def delete(self, campaign_id, ad_id):
        abort_if_campaign_or_ad_doesnt_exist(campaign_id, ad_id)
        ad_request = AdRequest.query.filter_by(campaign_id=campaign_id, id=ad_id).first_or_404()
        db.session.delete(ad_request)
        db.session.commit()
        return '', 204

class AdRequestListAPI(Resource):
    def get(self, campaign_id):
        abort_if_campaign_or_ad_doesnt_exist(campaign_id)
        ad_requests = AdRequest.query.filter_by(campaign_id=campaign_id).all()
        return jsonify([ad_request.to_dict() for ad_request in ad_requests])

