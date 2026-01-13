from fastapi.testclient import TestClient
from main import app
from database import SessionLocal, engine
import models

# Ensure we are using a clean DB or the seeded one
client = TestClient(app)

def test_read_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Welcome to the Gift Recommendation Service"}

def test_search_products_filter():
    # Test searching for 'Tech' category
    response = client.get("/search?category=Tech")
    assert response.status_code == 200
    results = response.json()
    assert len(results) > 0
    # Verify all results are indeed Tech
    for item in results:
        assert item["category"] == "Tech"

def test_search_products_price():
    # Test max price filter
    response = client.get("/search?maxPrice=30.00")
    assert response.status_code == 200
    results = response.json()
    for item in results:
        assert item["price"] <= 30.00

def test_recommendations_flow():
    payload = {
        "recipient_age": 25,
        "occasion": "Birthday",
        "relationship": "Friend",
        "budget": 100.0,
        "interests": ["music", "wireless"]
    }
    response = client.post("/recommendations", json=payload)
    assert response.status_code == 200
    data = response.json()
    
    # Should return a list
    assert isinstance(data, list)
    
    if len(data) > 0:
        top_pick = data[0]
        # Ensure the response structure is correct
        assert "score" in top_pick
        assert "reason" in top_pick
        assert "title" in top_pick
        # Since we asked for 'music'/'wireless', the score should be boosted
        assert top_pick["score"] >= 10