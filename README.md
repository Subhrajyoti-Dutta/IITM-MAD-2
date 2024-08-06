CREATE TABLE ad_request_2 (
ad_id INTEGER NOT NULL,
campaign_id INTEGER NOT NULL,
influencer_id INTEGER NOT NULL,
topic VARCHAR(20) NOT NULL,
messages TEXT,
requirements TEXT NOT NULL,
payment_amount FLOAT NOT NULL,
status VARCHAR(20) NOT NULL,
PRIMARY KEY (ad_id),
FOREIGN KEY(campaign_id) REFERENCES campaign (campaign_id),
FOREIGN KEY(influencer_id) REFERENCES influencer (influencer_id)
);

INSERT INTO ad_request_2
SELECT ad_request.ad_id, ad_request.campaign_id, ad_request.influencer_id, 'Youtube Sponsorship', ad_request.messages, ad_request.requirements, ad_request.payment_amount, ad_request.status
FROM ad_request;
