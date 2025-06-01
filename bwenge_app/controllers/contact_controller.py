from flask import Blueprint, request, jsonify
from bwenge_app.extensions import db
from bwenge_app.models.contact import Contact

contact_bp = Blueprint('contact', __name__, url_prefix='/api/v1/contact')

# Route to create a contact inquiry (Public access)
@contact_bp.route('/create', methods=['POST'])
def create_contact():
    data = request.get_json()
    name = data.get('name')
    email = data.get('email')
    message = data.get('message')

    if not name or not email or not message:
        return jsonify({'error': 'Name, email, and message are required'}), 400

    contact_message = Contact(name=name, email=email, message=message)
    db.session.add(contact_message)
    db.session.commit()

    return jsonify({'message': 'Contact inquiry submitted successfully', 'contact': contact_message.to_dict()}), 201

# Route to get all contact messages (Admin access only)
@contact_bp.route('/all', methods=['GET'])
def get_all_contacts():
    contacts = Contact.query.all()
    return jsonify({'contacts': [contact.to_dict() for contact in contacts]}), 200

# Route to get a single contact message by ID
@contact_bp.route('/get/<int:id>', methods=['GET'])
def get_contact(id):
    contact = Contact.query.get_or_404(id)
    return jsonify({'contact': contact.to_dict()}), 200

# Route to update a contact message
@contact_bp.route('/update/<int:id>', methods=['PUT'])
def update_contact(id):
    contact = Contact.query.get_or_404(id)
    data = request.get_json()

    contact.name = data.get('name', contact.name)
    contact.email = data.get('email', contact.email)
    contact.message = data.get('message', contact.message)

    db.session.commit()
    return jsonify({'message': 'Contact message updated successfully', 'contact': contact.to_dict()}), 200

# Route to delete a contact message
@contact_bp.route('/delete/<int:id>', methods=['DELETE'])
def delete_contact(id):
    contact = Contact.query.get_or_404(id)
    db.session.delete(contact)
    db.session.commit()
    return jsonify({'message': 'Contact message deleted'}), 200



# Route to get the count of all contact inquiries (Admin access)
@contact_bp.route('/count', methods=['GET'])
def get_contacts_count():
    try:
        count = Contact.query.count()
        return jsonify({"count": count}), 200
    except Exception as e:
        return jsonify({"error": "Error fetching contacts count", "details": str(e)}), 500
