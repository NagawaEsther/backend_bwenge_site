from flask import Blueprint, request, jsonify
from bwenge_app.extensions import db
from bwenge_app.models.application import Application

application_bp = Blueprint('application', __name__, url_prefix='/api/v1/application')

# Route to create an application (Public access)
@application_bp.route('/create', methods=['POST'])
def create_application():
    data = request.get_json()

    required_fields = ['full_name', 'email', 'phone_number', 'date_of_birth', 'gender',
                       'course_selection', 'address', 'guardian_name', 'guardian_contact']
    
    for field in required_fields:
        if not data.get(field):
            return jsonify({'error': f'{field.replace("_", " ").capitalize()} is required'}), 400

    application = Application(
        full_name=data['full_name'],
        email=data['email'],
        phone_number=data['phone_number'],
        date_of_birth=data['date_of_birth'],
        gender=data['gender'],
        course_selection=data['course_selection'],
        address=data['address'],
        guardian_name=data['guardian_name'],
        guardian_contact=data['guardian_contact']
    )

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
    data = request.get_json()

    for field in ['full_name', 'email', 'phone_number', 'date_of_birth', 'gender',
                  'course_selection', 'address', 'guardian_name', 'guardian_contact']:
        if field in data:
            setattr(application, field, data[field])

    db.session.commit()
    return jsonify({'message': 'Application updated successfully', 'application': application.to_dict()}), 200

# Route to delete an application
@application_bp.route('/delete/<int:id>', methods=['DELETE'])
def delete_application(id):
    application = Application.query.get_or_404(id)
    db.session.delete(application)
    db.session.commit()
    return jsonify({'message': 'Application deleted'}), 200

# Route to get the count of applications (Admin access)
@application_bp.route('/count', methods=['GET'])
def get_application_count():
    count = Application.query.count()
    return jsonify({'count': count}), 200