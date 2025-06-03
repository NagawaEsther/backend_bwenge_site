from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from bwenge_app.extensions import db

class Application(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(255), nullable=False)
    phone_number = db.Column(db.String(20), nullable=False)
    date_of_birth = db.Column(db.String(20), nullable=False)  # Consider changing to Date if validating
    gender = db.Column(db.String(10), nullable=False)
    course_selection = db.Column(db.String(100), nullable=False)
    address = db.Column(db.Text, nullable=False)
    guardian_name = db.Column(db.String(100), nullable=False)
    guardian_contact = db.Column(db.String(20), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            "id": self.id,
            "full_name": self.full_name,
            "email": self.email,
            "phone_number": self.phone_number,
            "date_of_birth": self.date_of_birth,
            "gender": self.gender,
            "course_selection": self.course_selection,
            "address": self.address,
            "guardian_name": self.guardian_name,
            "guardian_contact": self.guardian_contact,
            "created_at": self.created_at.strftime("%Y-%m-%d %H:%M:%S")
        }