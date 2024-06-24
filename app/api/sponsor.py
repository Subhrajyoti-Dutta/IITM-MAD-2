from flask import Blueprint, request, jsonify
from flask_restful import Resource, Api, abort
# from app import db
from app.models import db, Sponsor
import random

sponsor_blueprint = Blueprint('sponsors', __name__)
api = Api(sponsor_blueprint)

def abort_if_sponsor_doesnt_exist(sponsor_id):
    sponsor = Sponsor.query.get(sponsor_id)
    if not sponsor:
        abort(404, message=f"Sponsor {sponsor_id} doesn't exist")

class SponsorListAPI(Resource):
    def get(self):
        sponsors = Sponsor.query.all()
        return [sponsor.to_dict() for sponsor in sponsors]

class SponsorAPI(Resource):
    def get(self, sponsor_id):
        abort_if_sponsor_doesnt_exist(sponsor_id)
        sponsor = Sponsor.query.get(sponsor_id)
        return sponsor.to_dict()

    def post(self):
        data = request.get_json()
        if not data:
            abort(400, message="No input data provided")
        
        # Check for unique username
        if Sponsor.query.filter_by(username=data.get('Username')).first():
            abort(400, message="Username already exists")

        # Generate a unique ID
        while True:
            new_id = random.randint(1, 2**31 - 1)
            if not Sponsor.query.get(new_id):
                break
        
        new_sponsor = Sponsor(
            sponsor_id=new_id,
            username=data.get('Username'),
            password=data.get('Password'),  # This should be hashed in a real application
            full_name=data.get('Full_Name'),
            country_code=data.get('Country_Code'),
            phone=data.get('Phone'),
            company=data.get('Company'),
            industry=data.get('Industry')
        )
        
        db.session.add(new_sponsor)
        db.session.commit()
        
        return new_sponsor.to_dict(), 201

    def put(self, sponsor_id):
        abort_if_sponsor_doesnt_exist(sponsor_id)
        sponsor = Sponsor.query.get(sponsor_id)
        if not request.json:
            abort(400, message="No input data provided")
        
        data = request.get_json()
        sponsor.full_name = data.get('Full_Name', sponsor.full_name)
        sponsor.country_code = data.get('Country_Code', sponsor.country_code)
        sponsor.phone = data.get('Phone', sponsor.phone)
        sponsor.company = data.get('Company', sponsor.company)
        sponsor.industry = data.get('Industry', sponsor.industry)
        
        db.session.commit()
        return sponsor.to_dict()

    def delete(self, sponsor_id):
        abort_if_sponsor_doesnt_exist(sponsor_id)
        sponsor = Sponsor.query.get(sponsor_id)
        db.session.delete(sponsor)
        db.session.commit()
        return {'result': True}