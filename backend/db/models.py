from sqlalchemy import Column, Integer, String, DateTime, Numeric, JSON, func
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.dialects.postgresql import UUID
import uuid
from datetime import datetime

Base = declarative_base()

class LoyaltyAccount(Base):
    __tablename__ = 'loyalty_accounts'
    account_id = Column(String, primary_key=True, index=True)
    program_name = Column(String, index=True)
    current_balance = Column(Integer, default=0)
    last_updated = Column(DateTime, default=datetime.utcnow)
    metadata = Column(JSON, nullable=True)

class Recommendation(Base):
    __tablename__ = 'recommendations'
    id = Column(String, primary_key=True, index=True)
    title = Column(String)
    description = Column(String)
    program_name = Column(String)
    points_required = Column(Integer)
    estimated_value = Column(Integer)
    confidence_score = Column(Numeric, default=0)
