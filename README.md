# Gimmie Gift Recommendation Service

A production-ready backend service that ingests product data, allows searching/filtering, and provides "Best Pick" recommendations based on user interests and budget.

## 🚀 Features

* **Product Ingestion:** Automatic seeding of 50+ products into PostgreSQL.
* **Smart Search:** Filter by category, retailer, price, and text search (title/desc/tags).
* **Recommendation Engine:** Weighted scoring algorithm (+10 for interest match, +5 for occasion match).
* **Event Tracking:** Logs user interactions (clicks/views) to build a "learning" dataset for future personalization.
* **API Documentation:** Fully interactive Swagger UI.

## 🛠 Tech Stack

* **Language:** Python 3.10+
* **Framework:** FastAPI (High performance, easy documentation)
* **Database:** PostgreSQL
* **ORM:** SQLAlchemy
* **Validation:** Pydantic

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

The `/recommendations` endpoint uses a weighted scoring system:

1.  **Hard Filter:** Eliminates products above the `budget`.
2.  **Interest Scoring (+10 pts):** Checks if any of the user's `interests` appear in the product tags, title, or description.
3.  **Occasion Scoring (+5 pts):** Checks for keywords relevant to the occasion (e.g., "Birthday" -> checks for "party", "fun").
4.  **Learning Layer Boost (+3 pts):** Queries the `events` table to find the top 3 most popular categories globally. Any product in these trending categories receives a boost, ensuring the system "learns" from user engagement.
5.  **Sorting:** Products are returned in descending order of their total score.

### Search Relevance
When `sort=relevance` is used, results are ranked by where the keyword appears:
* **Title Match:** High priority (+3)
* **Tag Match:** Medium priority (+2)
* **Description Match:** Low priority (+1)
## 📈 Future Improvements

If given more time, I would improve:
* **Hybrid Search:** Implement vector embeddings (PGVector) for semantic search instead of simple keyword matching.
* **Caching:** Add Redis to cache search results for faster performance.
* **Authentication:** specific User IDs using JWT tokens instead of passing strings.