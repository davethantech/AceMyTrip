from sqlalchemy.orm import Session
from . import models
from datetime import datetime

def get_balances(db: Session):
    return db.query(models.LoyaltyAccount).all()

def get_recommendations(db: Session):
    return db.query(models.Recommendation).all()

def get_account_by_id(db: Session, account_id: str):
    return db.query(models.LoyaltyAccount).filter(models.LoyaltyAccount.account_id == account_id).first()

def update_account_sync(db: Session, account_id: str):
    acc = get_account_by_id(db, account_id)
    if acc:
        acc.last_updated = datetime.utcnow()
        db.add(acc)
        db.commit()
        db.refresh(acc)
    return acc

def search_recommendations(db: Session, query: str):
    q = query.lower()
    recs = db.query(models.Recommendation).all()
    matches = [r for r in recs if q in (r.title or '').lower() or q in (r.description or '').lower()]
    return matches
