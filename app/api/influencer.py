from flask import request, jsonify
from flask_restful import Resource, Api, abort
from app.models import *
import random

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
        
        data = request.get_json()
        
        influencer.full_name = data.get('Full_Name', influencer.full_name)
        influencer.country_code = data.get('Country_Code', influencer.country_code)
        influencer.phone = data.get('Phone', influencer.phone)
        influencer.niche = data.get('Niche', influencer.niche)
        influencer.reach = data.get('Reach', influencer.reach)
        influencer.bio = data.get('Bio', influencer.bio)
        
        platform = data.get('Platform', {})
        influencer.youtube = platform.get('Youtube', influencer.youtube)
        influencer.twitter = platform.get('Twitter', influencer.twitter)
        influencer.instagram = platform.get('Instagram', influencer.instagram)
        influencer.others = platform.get('Others', influencer.others)
        
        db.session.commit()
        return influencer.to_dict()

    def post(self):
        data = request.get_json()
        if not data:
            abort(400, message="No input data provided")
        
        # Check for unique username
        if Influencer.query.filter_by(username=data.get('Username')).first():
            abort(400, message="Username already exists")

        # Generate a unique ID
        while True:
            new_id = random.randint(1, 2**31 - 1)
            if not Influencer.query.get(new_id):
                break
        
        new_influencer = Influencer(
            influencer_id=new_id,
            username=data.get('Username'),
            password=data.get('Password'),  # This should be hashed in a real application
            full_name=data.get('Full_Name'),
            country_code=data.get('Country_Code'),
            phone=data.get('Phone'),
            niche=data.get('Niche'),
            reach=data.get('Reach', 0),
            bio=data.get('Bio', '-Blank-'),
            youtube=data.get('Platform', {}).get('Youtube', False),
            twitter=data.get('Platform', {}).get('Twitter', False),
            instagram=data.get('Platform', {}).get('Instagram', False),
            others=data.get('Platform', {}).get('Others', False)
        )
        
        db.session.add(new_influencer)
        db.session.commit()
        
        return new_influencer.to_dict(), 201

    def delete(self, influencer_id):
        abort_if_influencer_doesnt_exist(influencer_id)
        influencer = Influencer.query.get(influencer_id)
        db.session.delete(influencer)
        db.session.commit()
        return {'result': True}

    def delete(self, influencer_id):
        abort_if_influencer_doesnt_exist(influencer_id)
        influencer = Influencer.query.get(influencer_id)
        db.session.delete(influencer)
        db.session.commit()
        return {'result': True}
    
class InfluAdAPI(Resource):
    def get(self, influencer_id, status="all"):
        if status == "all":
            ad_requests = AdRequest.query.filter_by(influencer_id=influencer_id).all()
            return jsonify([ad_request.to_dict() for ad_request in ad_requests])
        else:
            ad_requests = AdRequest.query.filter_by(influencer_id=influencer_id, status=status).all()
            return jsonify([ad_request.to_dict() for ad_request in ad_requests])