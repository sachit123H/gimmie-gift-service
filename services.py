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
            .filter(models.Event.event_type == "click_out")
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

    # ============================================================
    # AI / EXPLANATION GENERATION STUB
    # ============================================================
    # NOTE: This section acts as a "Local Stub" for the AI requirement.
    # Instead of making an expensive latency-heavy call to OpenAI, 
    # we generate explanation text deterministically based on tags/rules.
    # To swap for real AI, we would replace the string formatting below 
    # with a call like: ai_service.generate_reason(product, profile)
    # ============================================================
    try:
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
        
        
        relationship_keywords = {
            "parent": ["home", "relaxation", "wellness", "kitchen"],
            "dad": ["home", "relaxation", "tech", "gadget"],
            "mom": ["home", "relaxation", "wellness", "beauty"],
            "partner": ["luxury", "romantic", "perfume", "jewelry", "spa"],
            "friend": ["fun", "gadget", "tech", "party"],
            "child": ["toy", "game", "play", "fun"]
        }
        # Flatten relationship string to a key (simple heuristic)
        relationship_aliases = {
            "parent": ["parent", "mother", "father", "mom", "dad"],
            "partner": ["partner", "spouse", "wife", "husband"],
            "friend": ["friend", "buddy"],
            "child": ["child", "kid", "son", "daughter"],
            "sibling": ["sibling", "brother", "sister"]
        }

        rel_key = None
        rel_value = profile.relationship.lower()

        for key, aliases in relationship_aliases.items():
            if any(alias in rel_value for alias in aliases):
                rel_key = key
                break

        rel_tags = relationship_keywords.get(rel_key, [])

        for p in products:
            score = 0
            reasons = []
            p_tags = p.tags.lower() if p.tags else ""
            p_title = p.title.lower()

            # Rule A: Interests (+10)
            for interest in profile.interests:
                
                p_desc = p.description.lower() if p.description else ""
                p_category = p.category.lower() if p.category else ""
                if (
                    interest.lower() in p_tags or 
                    interest.lower() in p_title or 
                    interest.lower() in p_desc or
                    interest.lower() == p_category
                    ):
                    score += 10
                    if f"Matches interest: {interest}" not in reasons:
                        reasons.append(f"This product matches the interest '{interest}'.")

            # Rule E: Age suitability (+1)
            if profile.recipient_age < 12 and p.category == "Toys":
                score += 1
                reasons.append("Appropriate for the recipient’s age.")
            # Rule B: Occasion (+5)
            for kw in relevant_keywords:
                if kw in p_tags or kw in p_title:
                    score += 5
                    reasons.append(f"Great for {profile.occasion}")
                    break 

            # Rule C: Learning Layer Boost (+3)
            if p.category in top_categories:
                score += 3
                reasons.append("This product is popular in a trending category.")

            # Rule D: Relationship Boost (+2)
            
            for r_tag in rel_tags:
                if r_tag in p_tags or r_tag in p_title:
                    score += 2
                    reasons.append(f"It is well-suited for a {profile.relationship.lower()}.")
                    break

            scored_products.append({
                "product": p,
                "score": score,
                # Deduplicate reasons and use new default string if empty
                "reason": " ".join(dict.fromkeys(reasons)) if reasons else "This product fits within the selected budget."
            })

        scored_products.sort(key=lambda x: x["score"], reverse=True)
        
        return [
            {
                "id": item["product"].id, 
                "title": item["product"].title, 
                "price": item["product"].price, 
                "score": item["score"], 
                "reason": item["reason"], 
                "image_url": item["product"].image_url,
                "url": item["product"].url  
            }
            for item in scored_products[:10]
        ]
        
    except SQLAlchemyError as e:
        
        print(f"Recommendation Engine Error: {e}")
        # Return empty list or handle gracefully instead of 500 Crash
        return []