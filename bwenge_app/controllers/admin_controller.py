from flask import Blueprint, request, jsonify
from bwenge_app.extensions import db
from bwenge_app.models.admin import Admin
from flask_jwt_extended import create_access_token

# Create a blueprint for admin routes
admin_bp = Blueprint('admin', __name__, url_prefix='/api/v1/auth')

# Route to create the admin account (if not already created)
@admin_bp.route('/create_admin', methods=['POST'])
def create_admin():
    # Call the create_admin method from the Admin model to handle admin creation
    Admin.create_admin()  # This method handles checking and creating the admin if needed

    return jsonify({"message": "Admin account created successfully."}), 201

# Route to authenticate admin login
@admin_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    # Fetch the admin record by username
    admin = Admin.query.filter_by(username=username).first()

    # Check if admin exists and if password matches the hash
    if admin and admin.check_password(password):
        # Generate JWT token
        access_token = create_access_token(identity=admin.id)  # You can use the admin ID or any identifier
        
        return jsonify({
            "message": "Login successful.",
            "access_token": access_token
        }), 200
    else:
        return jsonify({"message": "Invalid username or password."}), 401

# Register the admin blueprint
def register_admin_routes(app):
    app.register_blueprint(admin_bp)
