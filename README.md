# Gimmie Gift Recommendation Service

A production-ready backend service that ingests product data, allows searching/filtering, and provides "Best Pick" recommendations based on user interests and budget.

## 🚀 Features

* **Product Ingestion:** Automatic seeding of 50+ products into PostgreSQL.
* **Smart Search:** Filter by category, retailer, price, and text search (title/desc/tags).
* **Recommendation Engine:** Weighted scoring algorithm (+10 for interest match, +5 for occasion match, +2 for relationship).
* **Event Tracking:** Logs user interactions (clicks/views) to build a "learning" dataset for future personalization.
* **API Documentation:** Fully interactive Swagger UI.

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
    Access the API at: `http://127.0.0.1:8000/docs`

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
GET /search?category=Tech&maxPrice=50