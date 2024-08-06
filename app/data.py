import random
from datetime import datetime, timedelta
from app import db
from app.models import Influencer, Sponsor, Admin, Campaign, AdRequest, AdPerformance

# Helper function to generate random dates
def random_date(start, end):
    return start + timedelta(days=random.randint(0, int((end - start).days)))

# Create 100 Influencers
for i in range(4, 104):  # starting from 4 to avoid conflicts with existing entries
    influencer = Influencer(
        username=f"inf{i}",
        password="1234",
        full_name=f"Influencer {i}",
        country_code=91,
        phone=random.randint(1000000000, 9999999999),
        niche=random.choice(["Tech", "Fashion", "Travel", "Food", "Fitness"]),
        reach=random.randint(1000, 1000000),
        bio="-Blank-",
        youtube=bool(random.getrandbits(1)),
        twitter=bool(random.getrandbits(1)),
        instagram=bool(random.getrandbits(1)),
        others=bool(random.getrandbits(1)),
    )
    db.session.add(influencer)

# Create 100 Sponsors
for i in range(4, 104):  # starting from 4 to avoid conflicts with existing entries
    sponsor = Sponsor(
        username=f"spon{i}",
        password="1234",
        full_name=f"Sponsor {i}",
        country_code="91",
        phone=str(random.randint(1000000000, 9999999999)),
        company=f"Company {i}",
        industry=random.choice(["Tech", "Fashion", "Travel", "Food", "Fitness"]),
    )
    db.session.add(sponsor)

# Create 10 Admins
for i in range(3, 13):  # starting from 3 to avoid conflicts with existing entries
    admin = Admin(
        username=f"admin{i}",
        password="1234",
        full_name=f"Admin {i}",
        email=f"admin{i}@example.com",
        position="admin",
    )
    db.session.add(admin)

# Commit the new users to get their IDs
db.session.commit()

# Create Campaigns and AdRequests for Influencers and Sponsors
for sponsor in Sponsor.query.all():
    for _ in range(random.randint(1, 5)):  # Each sponsor can have 1 to 5 campaigns
        campaign = Campaign(
            name=f"Campaign {random.randint(1, 1000)}",
            sponsor_id=sponsor.sponsor_id,
            description="Promotion",
            start_date=random_date(datetime(2024, 1, 1), datetime(2024, 12, 31)),
            end_date=random_date(datetime(2024, 1, 1), datetime(2024, 12, 31)),
            budget=random.uniform(10000.0, 200000.0),
        )
        db.session.add(campaign)
        db.session.commit()  # Commit to get campaign ID

        for influencer in Influencer.query.all():
            for _ in range(random.randint(1, 3)):  # Each campaign can have 1 to 3 ad requests
                status = random.choice(["Active", "Completed", "Null", "Rejected"])
                ad_request = AdRequest(
                    campaign_id=campaign.campaign_id,
                    influencer_id=influencer.influencer_id,
                    topic=random.choice(["Youtube Sponsorship", "Poster Distribution", "Product Giveaway"]),
                    messages="Product Review",
                    requirements="20 Mins",
                    payment_amount=random.uniform(5000.0, 20000.0),
                    status=status,
                )
                db.session.add(ad_request)
                db.session.commit()  # Commit to get ad_request ID

                if status in ["Active", "Completed"]:
                    ad_performance = AdPerformance(
                        ad_id=ad_request.ad_id,
                        reach=random.randint(1000, 1000000),
                        posts=random.randint(1, 20),
                        likes=random.randint(100, 100000),
                        rating=random.randint(1, 5),
                    )
                    db.session.add(ad_performance)

# Commit all changes to the database
db.session.commit()
print("Database population complete.")
