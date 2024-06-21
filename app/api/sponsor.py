from flask import Blueprint, request, jsonify
from flask_restful import Resource, Api, abort
# from app import db
from app.models import db, Sponsor

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

    def post(self, sponsor_id):
        data = request.get_json()
        new_sponsor = Sponsor(
            id=sponsor_id,
            full_name=data.get('Full Name'),
            email=data.get('Email'),
            country_code=data.get('Country Code'),
            phone=data.get('Phone'),
            company=data.get('Company'),
            budget=data.get('Budget'),
            industry=data.get('Industry')
        )
        db.session.add(new_sponsor)
        db.session.commit()
        return jsonify(new_sponsor.to_dict())

    def put(self, sponsor_id):
        abort_if_sponsor_doesnt_exist(sponsor_id)
        sponsor = Sponsor.query.get(sponsor_id)
        data = request.get_json()
        sponsor.full_name = data.get('Full Name', sponsor.full_name)
        sponsor.email = data.get('Email', sponsor.email)
        sponsor.country_code = data.get('Country Code', sponsor.country_code)
        sponsor.phone = data.get('Phone', sponsor.phone)
        sponsor.company = data.get('Company', sponsor.company)
        sponsor.budget = data.get('Budget', sponsor.budget)
        sponsor.industry = data.get('Industry', sponsor.industry)
        db.session.commit()
        return jsonify(sponsor.to_dict())

    def delete(self, sponsor_id):
        abort_if_sponsor_doesnt_exist(sponsor_id)
        sponsor = Sponsor.query.get(sponsor_id)
        db.session.delete(sponsor)
        db.session.commit()
        return {'result': True}