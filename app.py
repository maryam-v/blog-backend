from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)

# --- Database config (SQLite for now) ---
# app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///app.db"

db_url = os.environ.get("DATABASE_URL", "sqlite:///app.db")

if db_url.startswith("postgres://"):
    db_url = db_url.replace("postgres://", "postgresql://", 1)

app.config["SQLALCHEMY_DATABASE_URI"] = db_url

app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

# --- Simple model ---
class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(200), nullable=False)

@app.route("/")
def home():
    return "Hello from Heroku with DB 🚀"

@app.route("/add")
def add_message():
    msg = Message(text="Hello database")
    db.session.add(msg)
    db.session.commit()
    return "Message added!"

@app.route("/messages")
def get_messages():
    messages = Message.query.all()
    return {"messages": [m.text for m in messages]}

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
