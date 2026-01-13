from sqlalchemy.orm import Session
from sqlalchemy import or_, func, desc
from sqlalchemy.exc import SQLAlchemyError
import models
import schemas

def get_relevance_score(product, query: str):
    """Calculates search relevance score (Title > Tags > Desc)."""
    score = 0
    term = query.lower()
    if term in product.title.lower(): score += 3
    if product.tags and term in product.tags.lower(): score += 2
    if product.description and term in product.description.lower(): score += 1
    return score

def get_top_categories(db: Session, limit: int = 3):
    """Fetches trending categories based on user interaction events."""
    try:
        category_stats = (
            db.query(models.Product.category, func.count(models.Event.id))
            .join(models.Event, models.Event.product_id == models.Product.id)
            .group_by(models.Product.category)
            .order_by(func.count(models.Event.id).desc())
            .limit(limit)
            .all()
        )
        return [cat for cat, count in category_stats]
    except SQLAlchemyError as e:
        print(f"Learning Layer Error: {e}")
        return []

def get_recommendations(profile: schemas.RecommendationRequest, db: Session):
    """
    Core Recommendation Engine Logic.
    Applies Hard Filters (SQL) -> Scoring (Python) -> Learning Boost.
    """
    # 1. Hard Filter: Budget & Interests (SQL Optimization)
    query = db.query(models.Product).filter(models.Product.price <= profile.budget)
    
    filters = []
    # Interest Matching
    for interest in profile.interests:
        term = f"%{interest}%"
        filters.append(models.Product.title.ilike(term))
        filters.append(models.Product.tags.ilike(term))
    
    # Occasion Matching (Keywords)
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
        
    if filters:
        query = query.filter(or_(*filters))
        
    products = query.all()
    
    # 2. Fetch Trending Categories (Learning Layer)
    top_categories = get_top_categories(db)

    # 3. Weighted Scoring
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
        for kw in relevant_keywords:
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
        {
            "id": item["product"].id, 
            "title": item["product"].title, 
            "price": item["product"].price, 
            "score": item["score"], 
            "reason": item["reason"], 
            "image_url": item["product"].image_url
        }
        for item in scored_products[:10]
    ]