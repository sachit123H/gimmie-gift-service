# Gimmie Gift Recommendation Service

A production-ready backend service that ingests product data, allows searching/filtering, and provides "Best Pick" recommendations based on user interests and budget.

## 🚀 Features

* **Product Ingestion:** Automatic seeding of 50 products into PostgreSQL.
* **Smart Search:** Filter by category, retailer, price, and text search (title/desc/tags).
* **Recommendation Engine:** Weighted scoring algorithm (+10 for interest match, +5 for occasion match, +2 for relationship).
* **Event Tracking:** Logs user interactions (clicks/views) to build a "learning" dataset for future personalization.
* **API Documentation:** Fully interactive Swagger UI.
* **UI Dashboard:** A simple frontend to visualize search and recommendations interactively.

## 🛠 Tech Stack

* **Language:** Python 3.10+
* **Framework:** FastAPI (High performance, easy documentation)
* **Database:** PostgreSQL
* **ORM:** SQLAlchemy
* **Architecture:** Service Layer Pattern with Pydantic Validation

## ⚙️ Setup Instructions

1.  **Clone the repository**
    ```bash
    git clone <your-repo-link>
    cd gimmie-gift-service
    ```

2.  **Install dependencies**
    ```bash
    python -m venv venv
    source venv/bin/activate  # (On Windows: venv\Scripts\activate)
    pip install -r requirements.txt
    ```

3.  **Configure Database**
    * Create a PostgreSQL database named `gimmie_db`.
    * Copy `.env.example` to `.env` and update your credentials:
        ```
        DATABASE_URL=postgresql://postgres:yourpassword@localhost/gimmie_db
        ```

4.  **Seed Data**
    Run the seed script to populate the database with mock products:
    ```bash
    python seed.py
    ```

5.  **Run the Server**
    ```bash
    uvicorn main:app --reload
    ```
    * Access the API at: `http://127.0.0.1:8000/docs`
    * Access the Dashboard at: `http://127.0.0.1:8000/dashboard`

## 🧠 Ranking Logic

The `/recommendations` endpoint uses a multi-factor weighted scoring system:

1.  **Hard Filter:** Eliminates products above the `budget`.
2.  **Interest Scoring (+10 pts):** Checks if any of the user's `interests` appear in the product tags, title, or description.
3.  **Occasion Scoring (+5 pts):** Contextual boost for keywords relevant to the occasion (e.g., "Birthday" -> "party", "fun").
4.  **Relationship Context (+2 pts):** Heuristic boost based on relationship type (e.g., "Parent" -> "home", "wellness").
5.  **Learning Layer Boost (+3 pts):** Queries the `events` table to find the top 3 most popular categories globally.
    * *Cold Start Strategy:* The system is designed to handle the "cold start" problem gracefully. If no event data exists (fresh install), the learning boost is simply skipped, relying on the core interest/occasion logic until data is gathered.

## 📡 API Examples

**Search for Tech products under $50:**
```bash
curl "[http://127.0.0.1:8000/search?category=Tech&maxPrice=50](http://127.0.0.1:8000/search?category=Tech&maxPrice=50)" 
```

**Get Recommendations:**

```bash
curl -X POST "[http://127.0.0.1:8000/recommendations](http://127.0.0.1:8000/recommendations)" \
     -H "Content-Type: application/json" \
     -d '{
           "recipient_age": 25,
           "occasion": "Birthday",
           "relationship": "Friend",
           "budget": 50,
           "interests": ["music", "tech"]
         }'
```
**🔮 Future Improvements & Tradeoffs**

While this MVP meets the core requirements, here is how I would approach scaling it for a production environment:

1.  **Async "Learning" Layer (Tradeoff):**
*  **Current State:* The system calculates trending categories in real-time during the recommendation request.
*  **Scalability Issue:* As event data grows to millions of rows, summing these aggregates on every request will increase latency.
*  **Improvement:* I would move the ``get_top_categories`` logic to a background job (using Celery or Redis) to pre-calculate trending tags periodically (e.g., every hour) rather than on every request.

2.  **Pagination:**
*  The current search endpoint returns all matches. For a larger dataset, implementing cursor-based or offset-based pagination is essential to reduce payload size and improve frontend performance.

3.  **Advanced Personalization:**
* Currently, the learning layer applies a global boost based on general popularity. With a user authentication system, I would implement collaborative filtering to recommend products based on similar users' behaviors, rather than just global trends.

4. **Infrastructure:**
* Containerize the application using Docker and deploy to an auto-scaling environment (like AWS ECS or Kubernetes) to handle variable traffic loads.

**🧭 How to Review This Project**

1. **Run the Server:** Follow the setup instructions above.with search and recommendations.
2. **Use the Dashboard:** Visit ``/dashboard`` to interact with search and recommendations visually.
3. **Generate Events:** Click on products in the dashboard to generate real user events.
4. **Observe Learning:** Inspect ``/recommendations/diagnostics`` to see how your interactions influence the "Trending Category" logic.