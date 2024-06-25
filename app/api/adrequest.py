from flask import Blueprint, request, jsonify, abort
from flask_restful import Resource, Api
from app.models import db, AdRequest, Campaign
import random

adrequest_bp = Blueprint('adrequests', __name__)
api = Api(adrequest_bp)

def abort_if_not_enough_budget(budget, campaign_id):
    campaign = Campaign.query.get(campaign_id)
    if budget > campaign.budget:
        abort(404, "Not enough Budget")
    else:
        campaign.budget -= budget
        return campaign.budget

def abort_if_campaign_or_ad_doesnt_exist(campaign_id, ad_id=None):
    campaign = Campaign.query.get(campaign_id)
    if not campaign:
        abort(404, message=f"Campaign {campaign_id} doesn't exist")
    if ad_id is not None:
        ad_request = AdRequest.query.filter_by(campaign_id=campaign_id, ad_id=ad_id).first()
        if not ad_request:
            abort(404, message=f"AdRequest {ad_id} in Campaign {campaign_id} doesn't exist")

class AdRequestAPI(Resource):
    def get(self, campaign_id, ad_id):
        abort_if_campaign_or_ad_doesnt_exist(campaign_id, ad_id)
        ad_request = AdRequest.query.filter_by(campaign_id=campaign_id, ad_id=ad_id).first()
        return ad_request.to_dict()

    def put(self, campaign_id, ad_id):
        print("Voila")
        abort_if_campaign_or_ad_doesnt_exist(campaign_id, ad_id)
        print("Voila2")
        ad_request = AdRequest.query.filter_by(campaign_id=campaign_id, ad_id=ad_id).first()
        print("Voila3")
        data = request.get_json()
        print("Voila4")
        print(data)
        print("Voila5")
        new_budget = abort_if_not_enough_budget(
            data.get('Payment_Amount', ad_request.payment_amount) - ad_request.payment_amount,
            campaign_id
        )
        print("Voila6")
        ad_request.influencer_id = data.get('Influencer_ID', ad_request.influencer_id)
        print("Voila7")
        ad_request.messages = data.get('Messages', ad_request.messages)
        print("Voila8")
        ad_request.requirements = data.get('Requirements', ad_request.requirements)
        print("Voila9")
        ad_request.payment_amount = data.get('Payment_Amount', ad_request.payment_amount)
        print("Voila10")
        ad_request.status = data.get('Status', ad_request.status)
        print("Voila11")

        db.session.commit()
        print("Voila12")
        res = ad_request.to_dict()
        print("Voila13")
        res["New Budget"] = new_budget
        return res, 201

    def post(self, campaign_id):
        abort_if_campaign_or_ad_doesnt_exist(campaign_id)
        data = request.get_json()
        new_budget = abort_if_not_enough_budget(
            data.get('Payment_Amount'),
            campaign_id
        )
        while True:
            new_id = random.randint(1, 2**31 - 1)
            if not AdRequest.query.filter_by(campaign_id=campaign_id, ad_id=new_id).first():
                break
        new_ad_request = AdRequest(
            ad_id=new_id,
            campaign_id=campaign_id,
            influencer_id=data.get('Influencer_ID'),
            messages=data.get('Messages'),
            requirements=data.get('Requirements'),
            payment_amount=data.get('Payment_Amount'),
            status="Null"
        )
        db.session.add(new_ad_request)
        db.session.commit()
        res = new_ad_request.to_dict()
        res["New Budget"] = new_budget
        return res, 201

    def delete(self, campaign_id, ad_id):
        abort_if_campaign_or_ad_doesnt_exist(campaign_id, ad_id)
        ad_request = AdRequest.query.filter_by(campaign_id=campaign_id, ad_id=ad_id).first()
        db.session.delete(ad_request)
        db.session.commit()
        return "Success", 204

class AdRequestListAPI(Resource):
    def get(self, campaign_id):
        abort_if_campaign_or_ad_doesnt_exist(campaign_id)
        ad_requests = AdRequest.query.filter_by(campaign_id=campaign_id).all()
        return jsonify([ad_request.to_dict() for ad_request in ad_requests])
