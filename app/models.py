from app import db
from flask_login import UserMixin

class Admin(db.Model, UserMixin):
    admin_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    full_name = db.Column(db.String(150))
    email = db.Column(db.String(150))
    position = db.Column(db.String(20), nullable=False)
    
    def get_id(self):
        return self.admin_id
    
    def to_dict(self):
        return {
            'Admin_ID': self.admin_id,
            'Username': self.username,
            'Full_Name': self.full_name,
            'Email': self.email,
            'Position': self.position
        }

class Influencer(db.Model, UserMixin):
    influencer_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
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
    flag = db.Column(db.Boolean, default=False, nullable=False)

    def get_id(self):
        return self.influencer_id
    
    def to_dict(self):
        return {
            'Influencer_ID': self.influencer_id,
            'Username': self.username,
            'Full_Name': self.full_name,
            'Country_Code': self.country_code,
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
    
    def _to_dict(self):
        return {
            'Influencer_ID': self.influencer_id,
            'Username': self.username,
            'Full_Name': self.full_name,
            'Country_Code': self.country_code,
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
            'Flag': self.flag,
        }

class Sponsor(db.Model, UserMixin):
    sponsor_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    full_name = db.Column(db.String(100), nullable=False)
    country_code = db.Column(db.String(10), nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    company = db.Column(db.String(100), nullable=False)
    industry = db.Column(db.String(100), nullable=False)
    flag = db.Column(db.Boolean, default=False, nullable=False)

    def get_id(self):
        return self.sponsor_id
    
    def to_dict(self):
        return {
            'Sponsor_ID': self.sponsor_id,
            'Username': self.username,
            'Full_Name': self.full_name,
            'Country_Code': self.country_code,
            'Phone': self.phone,
            'Company': self.company,
            'Industry': self.industry,
        }
    
    def _to_dict(self):
        return {
            'Sponsor_ID': self.sponsor_id,
            'Username': self.username,
            'Full_Name': self.full_name,
            'Country_Code': self.country_code,
            'Phone': self.phone,
            'Company': self.company,
            'Industry': self.industry,
            'Flag': self.flag,
        }

class Campaign(db.Model):
    campaign_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    sponsor_id = db.Column(db.Integer, db.ForeignKey('sponsor.sponsor_id'), nullable=False)
    description = db.Column(db.Text, nullable=False)
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date, nullable=False)
    budget = db.Column(db.Float, nullable=False)
    flag = db.Column(db.Boolean, default=False, nullable=False)

    def to_dict(self):
        return {
            'Campaign_ID': self.campaign_id,
            'Name': self.name,
            'Sponsor_ID': self.sponsor_id,
            'Description': self.description,
            'Start_Date': self.start_date.isoformat(),
            'End_Date': self.end_date.isoformat(),
            'Budget': self.budget,
        }
    
    def _to_dict(self):
        return {
            'Campaign_ID': self.campaign_id,
            'Name': self.name,
            'Sponsor_ID': self.sponsor_id,
            'Description': self.description,
            'Start_Date': self.start_date.isoformat(),
            'End_Date': self.end_date.isoformat(),
            'Budget': self.budget,
            'Flag': self.flag,
        }

class AdRequest(db.Model):
    ad_id = db.Column(db.Integer, primary_key=True)
    campaign_id = db.Column(db.Integer, db.ForeignKey('campaign.campaign_id'), nullable=False)
    influencer_id = db.Column(db.Integer, db.ForeignKey('influencer.influencer_id'), nullable=False)
    topic = db.Column(db.String(20), nullable=False)
    messages = db.Column(db.Text, nullable=True)
    requirements = db.Column(db.Text, nullable=False)
    payment_amount = db.Column(db.Float, nullable=False)
    status = db.Column(db.String(20), nullable=False)
    flag = db.Column(db.Boolean, default=False, nullable=False)

    def _to_dict(self):
        return {
            'Ad_ID': self.ad_id,
            'Influencer_ID': self.influencer_id,
            'Topic': self.topic,
            'Messages': self.messages,
            'Requirements': self.requirements,
            'Payment_Amount': self.payment_amount,
            'Status': self.status,
            'Flag': self.flag,
        }

    def to_dict(self):
        return {
            'Ad_ID': self.ad_id,
            'Campaign_ID': self.campaign_id,
            'Name': Campaign.query.get(self.campaign_id).name,
            'Influencer_ID': self.influencer_id,
            'Topic': self.topic,
            'Messages': self.messages,
            'Requirements': self.requirements,
            'Payment_Amount': self.payment_amount,
            'Status': self.status,
        }

class AdPerformance(db.Model):
    ad_id = db.Column(db.Integer, db.ForeignKey('ad_request.ad_id'), primary_key=True)
    reach = db.Column(db.Integer, nullable=False)
    posts = db.Column(db.Integer, nullable=False)
    likes = db.Column(db.Integer, nullable=False)
    rating = db.Column(db.Integer, nullable=False)

    def to_dict(self):
        return {
            'Ad_ID': self.ad_id,
            'Reach': self.reach,
            'Posts': self.posts,
            'Likes': self.likes,
            'Rating': self.rating,
        }
    