from fastapi import FastAPI, Depends, Query, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import or_, func, desc
from sqlalchemy.exc import SQLAlchemyError
from typing import Optional, List
from pydantic import BaseModel
from database import engine, get_db
import models

# Create tables
models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Gimmie AI Gift Service")

# --- Pydantic Models ---
class RecommendationRequest(BaseModel):
    recipient_age: int
    occasion: str
    relationship: str
    budget: float
    interests: List[str]

class EventRequest(BaseModel):
    user_id: str
    product_id: int
    event_type: str 

# --- Endpoints ---

@app.get("/")
def read_root():
    return {"message": "Welcome to the Gift Recommendation Service"}

@app.get("/search")
def search_products(
    q: Optional[str] = Query(None),
    category: Optional[str] = None,
    retailer: Optional[str] = None,
    min_price: Optional[float] = Query(None, alias="minPrice"),
    max_price: Optional[float] = Query(None, alias="maxPrice"),
    sort: Optional[str] = "relevance",
    db: Session = Depends(get_db)
):
    query = db.query(models.Product)
    
    # 1. Filtering
    if q:
        search_term = f"%{q}%"
        query = query.filter(or_(
            models.Product.title.ilike(search_term),
            models.Product.description.ilike(search_term),
            models.Product.tags.ilike(search_term)
        ))
    if category:
        query = query.filter(models.Product.category == category)
    if retailer:
        query = query.filter(models.Product.retailer == retailer)
    if min_price is not None:
        query = query.filter(models.Product.price >= min_price)
    if max_price is not None:
        query = query.filter(models.Product.price <= max_price)

    results = query.all()

    # 2. Sorting
    if sort == "price_asc":
        results.sort(key=lambda x: x.price)
    elif sort == "price_desc":
        results.sort(key=lambda x: x.price, reverse=True)
    elif sort == "relevance" and q:
        # Title match = 3 pts, Tag match = 2 pts, Desc match = 1 pt
        def get_relevance_score(product):
            score = 0
            term = q.lower()
            if term in product.title.lower(): score += 3
            if product.tags and term in product.tags.lower(): score += 2
            if product.description and term in product.description.lower(): score += 1
            return score
        
        results.sort(key=get_relevance_score, reverse=True)

    return results

@app.post("/recommendations")
def get_recommendations(profile: RecommendationRequest, db: Session = Depends(get_db)):
    # OPTIMIZATION: Instead of fetching ALL products <= budget, 
    # we filter in SQL for items that match at least ONE interest or the Occasion.
    # This prevents loading unrelated items into memory.
    
    query = db.query(models.Product).filter(models.Product.price <= profile.budget)
    
    filters = []
    
    # SQL Filter for Interests
    for interest in profile.interests:
        term = f"%{interest}%"
        filters.append(models.Product.title.ilike(term))
        filters.append(models.Product.tags.ilike(term))
        
    # SQL Filter for Occasion (add common keywords)
    occasion_keywords = {
        "birthday": ["party", "fun", "gift"],
        "anniversary": ["love", "romantic", "luxury"],
        "wedding": ["home", "kitchen", "decor"],
    }
    relevant_keywords = occasion_keywords.get(profile.occasion.lower(), [])
    for kw in relevant_keywords:
        term = f"%{kw}%"
        filters.append(models.Product.tags.ilike(term))
        filters.append(models.Product.title.ilike(term))
        
    # Apply the OR filter if we have any criteria
    if filters:
        query = query.filter(or_(*filters))
        
    products = query.all()
    
    # LEARNING LAYER
    top_categories = []
    try:
        category_stats = (
            db.query(models.Product.category, func.count(models.Event.id))
            .join(models.Event, models.Event.product_id == models.Product.id)
            .group_by(models.Product.category)
            .order_by(func.count(models.Event.id).desc())
            .limit(3)
            .all()
        )
        top_categories = [cat for cat, count in category_stats]
    except SQLAlchemyError as e:
        # Catch specific DB errors, log them, but don't crash the recommendation request
        print(f"Learning Layer Error: {e}")
        top_categories = []

    scored_products = []

    for p in products:
        score = 0
        reasons = []
        p_tags = p.tags.lower() if p.tags else ""
        p_title = p.title.lower()

        # Rule A: Interests (+10)
        for interest in profile.interests:
            if interest.lower() in p_tags or interest.lower() in p_title:
                score += 10
                if f"Matches interest: {interest}" not in reasons:
                    reasons.append(f"Matches interest: {interest}")

        # Rule B: Occasion (+5)
        # We re-check specific keywords here to apply the score accurately
        relevant = occasion_keywords.get(profile.occasion.lower(), [])
        for kw in relevant:
            if kw in p_tags or kw in p_title:
                score += 5
                reasons.append(f"Great for {profile.occasion}")
                break 

        # Rule C: Learning Layer Boost (+3)
        if p.category in top_categories:
            score += 3
            reasons.append("Trending category")

        scored_products.append({
            "product": p,
            "score": score,
            "reason": "; ".join(reasons) if reasons else "Fits within budget"
        })

    scored_products.sort(key=lambda x: x["score"], reverse=True)
    
    return [
        {"id": item["product"].id, "title": item["product"].title, "price": item["product"].price, 
         "score": item["score"], "reason": item["reason"], "image_url": item["product"].image_url}
        for item in scored_products[:10]
    ]

@app.post("/events")
def log_event(event: EventRequest, db: Session = Depends(get_db)):
    new_event = models.Event(
        user_id=event.user_id,
        product_id=event.product_id,
        event_type=event.event_type
    )
    db.add(new_event)
    db.commit()
    return {"message": "Event logged successfully"}

@app.get("/recommendations/diagnostics")
def get_diagnostics(user_id: Optional[str] = None, db: Session = Depends(get_db)):
    query = db.query(models.Event)
    if user_id:
        query = query.filter(models.Event.user_id == user_id)
    
    events = query.all()
    
    category_counts = {}
    for e in events:
        if e.product: 
            cat = e.product.category
            category_counts[cat] = category_counts.get(cat, 0) + 1
            
    return {
        "total_events": len(events),
        "top_categories_interacted": category_counts,
        "explanation": "Ranking logic currently boosts products in these categories by +3 points."
    }