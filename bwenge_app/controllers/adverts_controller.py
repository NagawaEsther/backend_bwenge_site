from flask import Blueprint, request, jsonify
from datetime import datetime
from bwenge_app.extensions import db
from bwenge_app.models.adverts import Advert

adverts_bp = Blueprint('adverts', __name__, url_prefix='/api/v1/adverts')

# Route to create an advert (Admin access, no authentication required)
@adverts_bp.route('/create', methods=['POST'])
def create_advert():
    data = request.get_json()

    title = data.get('title')
    description = data.get('description')
    image_url = data.get('image_url')
    expires_at = data.get('expires_at')

    if not title or not description:
        return jsonify({'error': 'Title and description are required'}), 400

    # Convert expires_at to datetime if provided
    expires_at_dt = datetime.strptime(expires_at, "%Y-%m-%d %H:%M:%S") if expires_at else None

    advert = Advert(
        title=title,
        description=description,
        image_url=image_url,
        expires_at=expires_at_dt
    )

    db.session.add(advert)
    db.session.commit()

    return jsonify(advert.to_dict()), 201


# Route to get all adverts (Public access)
@adverts_bp.route('/all', methods=['GET'])
def get_all_adverts():
    adverts = Advert.query.all()
    return jsonify([advert.to_dict() for advert in adverts]), 200


# Route to get a single advert by ID (Public access)
@adverts_bp.route('/advert/<int:id>', methods=['GET'])
def get_advert(id):
    advert = Advert.query.get_or_404(id)
    return jsonify(advert.to_dict()), 200


# Route to update an advert (Admin access, no authentication required)
@adverts_bp.route('/update/<int:id>', methods=['PUT'])
def update_advert(id):
    advert = Advert.query.get_or_404(id)
    data = request.get_json()

    advert.title = data.get('title', advert.title)
    advert.description = data.get('description', advert.description)
    advert.image_url = data.get('image_url', advert.image_url)

    expires_at = data.get('expires_at')
    if expires_at:
        advert.expires_at = datetime.strptime(expires_at, "%Y-%m-%d %H:%M:%S")

    db.session.commit()
    return jsonify(advert.to_dict()), 200


# Route to delete an advert (Admin access, no authentication required)
@adverts_bp.route('/delete/<int:id>', methods=['DELETE'])
def delete_advert(id):
    advert = Advert.query.get_or_404(id)
    db.session.delete(advert)
    db.session.commit()
    return jsonify({"message": "Advert deleted"}), 200
