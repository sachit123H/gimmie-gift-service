from fastapi.testclient import TestClient
from main import app

# Ensure we are using a clean DB or the seeded one
client = TestClient(app)

def test_read_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Welcome to the Gift Recommendation Service"}

# IMPROVEMENT: Added Health Check Test
def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}

def test_search_products_filter():
    response = client.get("/search?category=Tech")
    assert response.status_code == 200
    results = response.json()
    if len(results) > 0:
        for item in results:
            assert item["category"] == "Tech"

def test_search_products_price():
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
    
    assert isinstance(data, list)
    
    if len(data) > 0:
        top_pick = data[0]
        assert "score" in top_pick
        assert "reason" in top_pick
        assert top_pick["score"] >= 10