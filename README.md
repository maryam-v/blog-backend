# Blog Backend – Flask & SQLAlchemy

This repository contains the backend API for a simple blog application, built with **Flask** and **SQLAlchemy**.  
The backend exposes RESTful endpoints that are consumed by a **Next.js frontend**.

The application is deployed on **Heroku** and uses **PostgreSQL** as the database.

---

## 🚀 Features

- REST API for blog posts
- CRUD operations (Create, Read, Update, Delete)
- Flask + SQLAlchemy
- PostgreSQL (Heroku)
- Deployed on Heroku with Gunicorn
- CORS enabled for frontend integration
- Unit tests with pytest (SQLite in-memory)

---

## 🛠 Tech Stack

- Python
- Flask
- SQLAlchemy
- PostgreSQL
- Gunicorn
- Heroku

---

## 📌 API Endpoints

| Method | Endpoint           | Description            |
|------|--------------------|------------------------|
| GET  | `/posts`           | Get all blog posts     |
| GET  | `/posts/<id>`      | Get a single post      |
| POST | `/posts`           | Create a new post      |
| PUT  | `/posts/<id>`      | Update a post          |
| DELETE | `/posts/<id>`    | Delete a post          |

All endpoints return JSON responses.

---

## ▶️ Run Locally

### 1. Clone the repository
```bash
git clone https://github.com/YOUR_USERNAME/blog_backend.git
cd blog_backend
```

### 2. Create and activate a virtual environment
```bash
python -m venv venv
source venv/bin/activate   # macOS / Linux
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Run the application

```bash
python app.py
```
The backend will run on:

```
http://localhost:5001
```

---

## 🧪 Unit Tests

Basic unit tests are implemented using pytest to validate the core API endpoints.

### Run tests locally

```bash
pytest -q
```

Tests run against an in-memory SQLite database and do not affect production data.

---

## 🌍 Deployment (Heroku)

The backend is deployed on Heroku.

### 👉 Live Backend URL (Heroku):
https://flasker60-6ecec4d890e9.herokuapp.com


### Prerequisites

- Install Heroku CLI (Dev Center instructions):
https://devcenter.heroku.com/articles/heroku-cli
- Login:

```bash
heroku login
```

#### 1) Add required files for Heroku

##### Install Gunicorn and DB driver

```bash
pip install gunicorn psycopg2-binary
pip freeze > requirements.txt
```

##### Add a Procfile (tells Heroku how to run the app)

Create a file named Procfile (no extension) containing:

```bash
web: gunicorn app:app
```

This assumes your Flask instance is named app inside app.py.

#### 2) Create a Heroku app

```bash
heroku create app-name
```
#### 3) Add a PostgreSQL database

```bash
heroku addons:create heroku-postgresql:essential-0 --app app-name
```

#### 4) Configure the database URL in Flask

Heroku automatically provides DATABASE_URL.

To view it:

```bash
heroku config:get DATABASE_URL --app app-name
```

In your Flask code, you should read it from the environment (recommended):

- Use os.environ.get("DATABASE_URL")

- (If needed) replace postgres:// with postgresql:// for SQLAlchemy

#### 5) Deploy to Heroku (and update after changes)

##### First-time setup: add Heroku remote (only once)

If you created the app with heroku create, the remote is usually added automatically.
If not:

```bash
heroku git:remote -a app-name
```

##### Deploy / update workflow (same every time)
```bash
git add .
git commit -m "Update backend"
git push heroku main
```

#### 6) Quick troubleshooting

Check logs:

```bash
heroku logs --tail --app app-name
```


---

## 📝 Notes

The backend is designed to be consumed by a frontend built with Next.js, React, and Tailwind CSS.

---
