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
    def get(self, id):
        abort_if_campaign_doesnt_exist(id)
        campaign = Campaign.query.get(id)
        return jsonify(campaign.to_dict())

    def put(self, id):
        abort_if_campaign_doesnt_exist(id)
        campaign = Campaign.query.get(id)
        data = request.get_json()

        campaign.name = data.get('Name', campaign.name)
        campaign.description = data.get('Description', campaign.description)
        campaign.start_date = datetime.strptime(
            data.get('Start Date', campaign.start_date.isoformat()), '%Y-%m-%d').date()
        campaign.end_date = datetime.strptime(
            data.get('End Date', campaign.end_date.isoformat()), '%Y-%m-%d').date()
        campaign.budget = data.get('Budget', campaign.budget)

        db.session.commit()
        return jsonify(campaign.to_dict())

    def post(self):
        data = request.get_json()
        while True:
            new_id = random.randint(1, 2**31 - 1)
            if not Campaign.query.get(new_id):
                break
        new_campaign = Campaign(
            id = new_id,
            name=data.get('Name'),
            description=data.get('Description'),
            start_date=datetime.strptime(data.get('Start Date'), '%Y-%m-%d').date(),
            end_date=datetime.strptime(data.get('End Date'), '%Y-%m-%d').date(),
            budget=data.get('Budget'),
        )
        print(new_campaign.to_dict())
        db.session.add(new_campaign)
        db.session.commit()
        return jsonify(new_campaign.to_dict()), 201

    def delete(self, id):
        abort_if_campaign_doesnt_exist(id)
        campaign = Campaign.query.get(id)
        db.session.delete(campaign)
        db.session.commit()
        return '', 204

class CampaignListAPI(Resource):
    def get(self):
        campaigns = Campaign.query.all()
        return jsonify([campaign.to_dict() for campaign in campaigns])

