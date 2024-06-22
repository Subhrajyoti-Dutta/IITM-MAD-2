from app import db
from flask_login import UserMixin

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    role = db.Column(db.String(20), nullable=False)

    def to_dict(self):
        return {
            'ID': self.id,
            'Username': self.username,
            'Role': self.role
        }

class Influencer(db.Model):
    id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    full_name = db.Column(db.String(150))
    country_code = db.Column(db.Integer)
    phone = db.Column(db.Integer)
    niche = db.Column(db.String(150), default="Others")
    reach = db.Column(db.Integer, default=0)
    bio = db.Column(db.Text, default="-Blank-")
    youtube = db.Column(db.Boolean, default=False)
    twitter = db.Column(db.Boolean, default=False)
    instagram = db.Column(db.Boolean, default=False)
    others = db.Column(db.Boolean, default=False)

    def to_dict(self):
        return {
            'ID': self.id,
            'Full Name': self.full_name,
            'Country Code': self.country_code,
            'Phone': self.phone,
            'Niche': self.niche,
            'Reach': self.reach,
            'Platform' : {
                'Youtube': self.youtube,
                'Twitter': self.twitter,
                'Instagram': self.instagram,
                'Others': self.others
            },
            'Bio': self.bio,
        }

class Sponsor(db.Model):
    __tablename__ = 'sponsors'
    
    id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    full_name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    country_code = db.Column(db.String(10), nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    company = db.Column(db.String(100), nullable=False)
    industry = db.Column(db.String(100), nullable=False)

    def to_dict(self):
        return {
            'ID': self.id,
            'Full Name': self.full_name,
            'Email': self.email,
            'Country Code': self.country_code,
            'Phone': self.phone,
            'Company': self.company,
            'Industry': self.industry,
        }

class Campaign(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date, nullable=False)
    budget = db.Column(db.Float, nullable=False)

    def to_dict(self):
        return {
            'ID': self.id,
            'Name': self.name,
            'Description': self.description,
            'Start Date': self.start_date.isoformat(),
            'End Date': self.end_date.isoformat(),
            'Budget': self.budget,
        }

class AdRequest(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    campaign_id = db.Column(db.Integer, db.ForeignKey('campaign.id'), nullable=False)
    influencer_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    messages = db.Column(db.Text, nullable=True)
    requirements = db.Column(db.Text, nullable=False)
    payment_amount = db.Column(db.Float, nullable=False)
    status = db.Column(db.String(20), nullable=False)

    def to_dict(self):
        return {
            'id': self.id,
            'campaign_id': self.campaign_id,
            'influencer_id': self.influencer_id,
            'messages': self.messages,
            'requirements': self.requirements,
            'payment_amount': self.payment_amount,
            'status': self.status,
        }