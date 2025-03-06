from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from bwenge_app.extensions import db

class Subscribe(db.Model):
    __tablename__ = 'subscribers'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), nullable=False, unique=True)
    subscribed_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __init__(self, email):
        self.email = email

    def __repr__(self):
        return f"<Subscriber {self.email}>"
