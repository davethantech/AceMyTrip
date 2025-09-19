# Seed initial data into the database file (sqlite by default)
from db import database, models
from sqlalchemy.orm import Session
db = next(database.get_db())

# Check if data exists
if db.query(models.LoyaltyAccount).count() == 0:
    accounts = [
        models.LoyaltyAccount(account_id='1', program_name='amex', current_balance=80000, metadata={'elite_status':'Platinum'}),
        models.LoyaltyAccount(account_id='2', program_name='united', current_balance=45000, metadata={'elite_status':'Premier Gold'}),
        models.LoyaltyAccount(account_id='3', program_name='marriott', current_balance=120000, metadata={'elite_status':'Titanium'}),
    ]
    db.add_all(accounts)
if db.query(models.Recommendation).count() == 0:
    recs = [
        models.Recommendation(id='1', title='Use 50K Amex for a United flight worth $1,200', description='Transfer Amex points to United MileagePlus at 1:1 ratio. Book business class for great value.', program_name='amex', points_required=50000, estimated_value=1200, confidence_score=0.95),
        models.Recommendation(id='2', title='Paris Business Class - Air France', description='Use 63K United miles for LAX-CDG in business class.', program_name='united', points_required=63000, estimated_value=2400, confidence_score=0.92),
    ]
    db.add_all(recs)
db.commit()
print('Seeded data')