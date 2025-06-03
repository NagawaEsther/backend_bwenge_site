from flask import Blueprint, request, jsonify
from bwenge_app.extensions import db
from bwenge_app.models.application import Application

application_bp = Blueprint('application', __name__, url_prefix='/api/v1/application')

# Route to create an application (Public access)
@application_bp.route('/create', methods=['POST'])
def create_application():
    data = request.get_json(force=True)  # force JSON parsing
    
    # Map frontend keys to backend model keys
    mapped_data = {
        'full_name': data.get('fullName'),
        'email': data.get('email'),
        'phone_number': data.get('phone'),
        'date_of_birth': data.get('dob'),
        'gender': data.get('gender'),
        'course_selection': data.get('course'),
        'address': data.get('address'),
        'guardian_name': data.get('guardianName'),
        'guardian_contact': data.get('guardianContact')
    }

    # Validate required fields
    missing_fields = [field for field, value in mapped_data.items() if not value]
    if missing_fields:
        return jsonify({'error': f'Missing fields: {missing_fields}'}), 400

    application = Application(**mapped_data)

    db.session.add(application)
    db.session.commit()

    return jsonify({'message': 'Application submitted successfully', 'application': application.to_dict()}), 201

# Route to get all applications (Admin access)
@application_bp.route('/all', methods=['GET'])
def get_all_applications():
    applications = Application.query.all()
    return jsonify({'applications': [app.to_dict() for app in applications]}), 200

# Route to get a single application
@application_bp.route('/get/<int:id>', methods=['GET'])
def get_application(id):
    application = Application.query.get_or_404(id)
    return jsonify({'application': application.to_dict()}), 200

# Route to update an application
@application_bp.route('/update/<int:id>', methods=['PUT'])
def update_application(id):
    application = Application.query.get_or_404(id)
    data = request.get_json(force=True)

    # Map frontend keys to model attributes
    field_map = {
        'fullName': 'full_name',
        'email': 'email',
        'phone': 'phone_number',
        'dob': 'date_of_birth',
        'gender': 'gender',
        'course': 'course_selection',
        'address': 'address',
        'guardianName': 'guardian_name',
        'guardianContact': 'guardian_contact'
    }

    for front_key, model_field in field_map.items():
        if front_key in data:
            setattr(application, model_field, data[front_key])

    db.session.commit()
    return jsonify({'message': 'Application updated successfully', 'application': application.to_dict()}), 200

# Route to delete an application
@application_bp.route('/delete/<int:id>', methods=['DELETE'])
def delete_application(id):
    application = Application.query.get_or_404(id)
    db.session.delete(application)
    db.session.commit()
    return jsonify({'message': 'Application deleted'}), 200
