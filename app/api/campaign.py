from flask import Blueprint, request, jsonify
from flask_restful import Resource, Api, abort
from app.models import db, Campaign
import random
from datetime import datetime

campaign_blueprint = Blueprint('campaigns', __name__)
api = Api(campaign_blueprint)

def abort_if_campaign_doesnt_exist(campaign_id):
    campaign = Campaign.query.get(campaign_id)
    if not campaign:
        abort(404, message=f"Campaign {campaign_id} doesn't exist")


class CampaignAPI(Resource):
    def get(self, campaign_id):
        abort_if_campaign_doesnt_exist(campaign_id)
        campaign = Campaign.query.get(campaign_id)
        return jsonify(campaign.to_dict())

    def put(self, campaign_id):
        abort_if_campaign_doesnt_exist(campaign_id)
        campaign = Campaign.query.get(campaign_id)
        if not request.json:
            abort(400, message="No input data provided")
        
        data = request.get_json()

        campaign.name = data.get('Name', campaign.name)
        campaign.description = data.get('Description', campaign.description)
        campaign.start_date = datetime.strptime(
            data.get('Start_Date', campaign.start_date.isoformat()), '%Y-%m-%d').date()
        campaign.end_date = datetime.strptime(
            data.get('End_Date', campaign.end_date.isoformat()), '%Y-%m-%d').date()
        campaign.budget = data.get('Budget', campaign.budget)

        db.session.commit()
        return jsonify(campaign.to_dict())

    def post(self):
        data = request.get_json()
        if not data:
            abort(400, message="No input data provided")

        # Generate a unique ID
        while True:
            new_id = random.randint(1, 2**31 - 1)
            if not Campaign.query.get(new_id):
                break
        
        new_campaign = Campaign(
            campaign_id=new_id,
            name=data.get('Name'),
            sponsor_id=data.get('Sponsor_ID'),
            description=data.get('Description'),
            start_date=datetime.strptime(data.get('Start_Date'), '%Y-%m-%d').date(),
            end_date=datetime.strptime(data.get('End_Date'), '%Y-%m-%d').date(),
            budget=data.get('Budget')
        )
        
        db.session.add(new_campaign)
        db.session.commit()
        
        return new_campaign.to_dict(), 201

    def delete(self, campaign_id):
        abort_if_campaign_doesnt_exist(campaign_id)
        campaign = Campaign.query.get(campaign_id)
        db.session.delete(campaign)
        db.session.commit()
        return 'Success', 204

class CampaignListAPI(Resource):
    def get(self):
        campaigns = Campaign.query.all()
        return jsonify([campaign.to_dict() for campaign in campaigns])

