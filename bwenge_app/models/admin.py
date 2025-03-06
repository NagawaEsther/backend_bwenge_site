from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from bwenge_app.extensions import db
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt()  # Initialize bcrypt

class Admin(db.Model):
    __tablename__ = 'admins'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)  # Store hashed password
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, onupdate=datetime.utcnow)
    
    def __init__(self, username, password_hash):
        self.username = username
        self.password_hash = password_hash
    
    def check_password(self, password):
        """Check if the provided password matches the stored hashed password."""
        return bcrypt.check_password_hash(self.password_hash, password)
    
    @classmethod
    def create_admin(cls):
        """Create an admin user with a hashed password if it doesn't already exist."""
        # Check if the admin user already exists
        admin = Admin.query.filter_by(username='BwengeAdmin').first()

        if not admin:
            # Create the admin with a plain password first
            plain_password = 'Bwenge@256'  # This is the plain password before hashing
            hashed_password = bcrypt.generate_password_hash(plain_password).decode('utf-8')  # Hash the password
            
            # Create the admin instance with the hashed password
            admin = Admin(username='BwengeAdmin', password_hash=hashed_password)
            db.session.add(admin)
            db.session.commit()
            print("Admin account created successfully.")
        else:
            print("Admin account already exists.")
    
    def __repr__(self):
        return f"<Admin {self.username}>"
