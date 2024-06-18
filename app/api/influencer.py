from flask import request
from flask_restful import Resource, Api, abort
from app.models import db, Influencer

def abort_if_influencer_doesnt_exist(influencer_id):
    influencer = Influencer.query.get(influencer_id)
    if not influencer:
        abort(404, message=f"Influencer {influencer_id} doesn't exist")

class InfluencerListAPI(Resource):
    def get(self):
        influencers = Influencer.query.all()
        return [influencer.to_dict() for influencer in influencers]

class InfluencerAPI(Resource):
    def get(self, influencer_id):
        abort_if_influencer_doesnt_exist(influencer_id)
        influencer = Influencer.query.get(influencer_id)
        return influencer.to_dict()

    def put(self, influencer_id):
        abort_if_influencer_doesnt_exist(influencer_id)
        influencer = Influencer.query.get(influencer_id)
        if not request.json:
            abort(400, message="No input data provided")
        
        influencer.full_name = request.json.get('Full Name', influencer.full_name)
        influencer.country_code = request.json.get('Country Code', influencer.country_code)
        influencer.phone = request.json.get('Phone', influencer.phone)
        influencer.niche = request.json.get('Niche', influencer.niche)
        influencer.reach = request.json.get('Reach', influencer.reach)
        influencer.bio = request.json.get('Bio', influencer.bio)
        influencer.youtube = request.json.get('Platform').get('Youtube', influencer.youtube)
        influencer.twitter = request.json.get('Platform').get('Twitter', influencer.twitter)
        influencer.instagram = request.json.get('Platform').get('Instagram', influencer.instagram)
        influencer.others = request.json.get('Platform').get('Others', influencer.others)
        
        db.session.commit()
        return influencer.to_dict()

    def delete(self, influencer_id):
        abort_if_influencer_doesnt_exist(influencer_id)
        influencer = Influencer.query.get(influencer_id)
        db.session.delete(influencer)
        db.session.commit()
        return {'result': True}
