from fastapi import FastAPI, Depends, Query
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from sqlalchemy import or_
from typing import Optional
from database import engine, get_db
import models
import schemas
import services


models.Base.metadata.create_all(bind=engine)


app = FastAPI(title="Gimmie AI Gift Service")


# This tells FastAPI to look in the "static" folder for files when "/static" is requested
app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get("/dashboard")
async def read_dashboard():
    return FileResponse('static/index.html')

# --- API Endpoints ---

@app.get("/")
def read_root():
    return {"message": "Welcome to the Gift Recommendation Service"}

@app.get("/health")
def health_check():
    """Simple health check for load balancers/uptime monitors."""
    return {"status": "ok"}

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
    
    # Filtering logic
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

    # Sorting Logic
    if sort == "price_asc":
        results.sort(key=lambda x: x.price)
    elif sort == "price_desc":
        results.sort(key=lambda x: x.price, reverse=True)
    elif sort == "relevance" and q:
        # Uses the scoring logic from services.py
        results.sort(key=lambda x: services.get_relevance_score(x, q), reverse=True)

    return results

@app.post("/recommendations", response_model=list[schemas.RecommendationItem])
def get_recommendations(profile: schemas.RecommendationRequest, db: Session = Depends(get_db)):
    # Delegates complex logic to the service layer
    return services.get_recommendations(profile, db)

@app.post("/events")
def log_event(event: schemas.EventRequest, db: Session = Depends(get_db)):
    new_event = models.Event(
        user_id=event.user_id,
        product_id=event.product_id,
        event_type=event.event_type.value
    )
    db.add(new_event)
    db.commit()

    # Lightweight observability log (safe, non-intrusive)
    print(
        f"[EVENT] type={event.event_type.value} "
        f"user={event.user_id} "
        f"product={event.product_id}"
    )

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