URL Shortener API
A simple and fast URL shortener REST API built with FastAPI and SQLAlchemy.

Features
Short Link Generation: Generate unique short codes for long URLs.
Redirection: Automatically redirect short links to original destinations.
Click Analytics: Track the total number of visits per link.
Link Deletion: Instantly remove short URLs from the database.
Interactive Docs: Integrated Swagger UI for testing API endpoints.

Tech Stack
Python
FastAPI
Uvicorn
SQLAlchemy (SQLite)

Getting Started
Clone the repository:

git clone https://github.com/Kyotto-byte/UrlTool.git
cd UrlTool
Install dependencies:

pip install fastapi uvicorn sqlalchemy
Run the server:

python -m uvicorn UrlShortener:app --reload
Access documentation:
Open http://127.0.0.1:8000/docs in your browser to test the API endpoints.
