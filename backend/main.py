from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List
import os
from db import models, crud, schemas
from db.database import engine, get_db, init_db

app = FastAPI(title='AceMyTravel API')

app.add_middleware(CORSMiddleware, allow_origins=['*'], allow_methods=['*'], allow_headers=['*'])

# Initialize DB (create tables)
init_db()

@app.get('/api/loyalty/balances', response_model=List[schemas.LoyaltyAccount])
def get_balances(db=Depends(get_db)):
    return crud.get_balances(db)

@app.get('/api/optimize/recommendations', response_model=List[schemas.Recommendation])
def get_recommendations(db=Depends(get_db)):
    return crud.get_recommendations(db)

class QueryIn(BaseModel):
    query: str

@app.post('/api/optimize/query')
def post_query(q: QueryIn, db=Depends(get_db)):
    # Very simple search: return recommendations containing keywords
    recs = crud.search_recommendations(db, q.query)
    total = sum([r.estimated_value for r in recs])
    return {'original_query': q.query, 'recommendations': recs, 'total_value': total}

@app.post('/api/loyalty/sync/{account_id}')
def sync_account(account_id: str, db=Depends(get_db)):
    # Simulate a sync job by updating last_synced timestamp
    acc = crud.get_account_by_id(db, account_id)
    if not acc:
        raise HTTPException(status_code=404, detail='Account not found')
    crud.update_account_sync(db, account_id)
    return {'status': 'sync_triggered'}
