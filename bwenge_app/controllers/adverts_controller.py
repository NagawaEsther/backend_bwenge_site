# from flask import Blueprint, request, jsonify
# from datetime import datetime
# from bwenge_app.extensions import db
# from bwenge_app.models.adverts import Advert

# adverts_bp = Blueprint('adverts', __name__, url_prefix='/api/v1/adverts')

# # Route to create an advert (Admin access, no authentication required)
# @adverts_bp.route('/create', methods=['POST'])
# def create_advert():
#     data = request.get_json()

#     title = data.get('title')
#     description = data.get('description')
#     image_url = data.get('image_url')
#     expires_at = data.get('expires_at')

#     if not title or not description:
#         return jsonify({'error': 'Title and description are required'}), 400

#     # Convert expires_at to datetime if provided
#     expires_at_dt = datetime.strptime(expires_at, "%Y-%m-%d %H:%M:%S") if expires_at else None

#     advert = Advert(
#         title=title,
#         description=description,
#         image_url=image_url,
#         expires_at=expires_at_dt
#     )

#     db.session.add(advert)
#     db.session.commit()

#     return jsonify(advert.to_dict()), 201


# # Route to get all adverts (Public access)
# @adverts_bp.route('/all', methods=['GET'])
# def get_all_adverts():
#     adverts = Advert.query.all()
#     return jsonify([advert.to_dict() for advert in adverts]), 200


# # Route to get a single advert by ID (Public access)
# @adverts_bp.route('/advert/<int:id>', methods=['GET'])
# def get_advert(id):
#     advert = Advert.query.get_or_404(id)
#     return jsonify(advert.to_dict()), 200


# # Route to update an advert (Admin access, no authentication required)
# @adverts_bp.route('/update/<int:id>', methods=['PUT'])
# def update_advert(id):
#     advert = Advert.query.get_or_404(id)
#     data = request.get_json()

#     advert.title = data.get('title', advert.title)
#     advert.description = data.get('description', advert.description)
#     advert.image_url = data.get('image_url', advert.image_url)

#     expires_at = data.get('expires_at')
#     if expires_at:
#         advert.expires_at = datetime.strptime(expires_at, "%Y-%m-%d %H:%M:%S")

#     db.session.commit()
#     return jsonify(advert.to_dict()), 200


# # Route to delete an advert (Admin access, no authentication required)
# @adverts_bp.route('/delete/<int:id>', methods=['DELETE'])
# def delete_advert(id):
#     advert = Advert.query.get_or_404(id)
#     db.session.delete(advert)
#     db.session.commit()
#     return jsonify({"message": "Advert deleted"}), 200


from flask import Blueprint, request, jsonify, send_from_directory
from flask_jwt_extended import jwt_required, get_jwt_identity
from werkzeug.utils import secure_filename
from datetime import datetime
import os
from bwenge_app.extensions import db
from bwenge_app.models.adverts import Advert

adverts_bp = Blueprint('adverts', __name__, url_prefix='/api/v1/adverts')

# Configure upload folder and allowed extensions
UPLOAD_FOLDER = r'C:\news\adverts_images'  # Dedicated folder for advert images
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

# Ensure the upload folder exists
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Route to serve images
@adverts_bp.route('/images/<filename>', methods=['GET'])
def serve_image(filename):
    return send_from_directory(UPLOAD_FOLDER, filename)

# Route to create an advert (Admin access required)
@adverts_bp.route('/create', methods=['POST'])
@jwt_required()
def create_advert():
    try:
        current_user = get_jwt_identity()

        # Check if it's a form submission with file or a JSON request
        if request.content_type and 'multipart/form-data' in request.content_type:
            # Handle form data with file upload
            title = request.form.get('title')
            description = request.form.get('description')
            expires_at = request.form.get('expires_at')

            if not title or not description:
                return jsonify({"error": "Title and description are required"}), 400

            # Handle image upload if present (optional)
            image_filename = None
            if 'image' in request.files:
                file = request.files['image']
                if file and allowed_file(file.filename):
                    filename = secure_filename(file.filename)
                    file_path = os.path.join(UPLOAD_FOLDER, filename)
                    file.save(file_path)
                    image_filename = filename

            # Convert expires_at to datetime if provided
            expires_at_dt = datetime.strptime(expires_at, "%Y-%m-%d %H:%M:%S") if expires_at else None

            advert = Advert(
                title=title,
                description=description,
                image_url=image_filename,
                expires_at=expires_at_dt
            )
        else:
            # Handle JSON data without file
            data = request.get_json()
            if not data.get('title') or not data.get('description'):
                return jsonify({"error": "Title and description are required"}), 400

            expires_at = data.get('expires_at')
            expires_at_dt = datetime.strptime(expires_at, "%Y-%m-%d %H:%M:%S") if expires_at else None

            advert = Advert(
                title=data.get('title'),
                description=data.get('description'),
                image_url=data.get('image_url'),
                expires_at=expires_at_dt
            )

        db.session.add(advert)
        db.session.commit()

        return jsonify({
            "message": "Advert created successfully",
            "id": advert.id,
            "image_url": advert.image_url
        }), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": "Error occurred", "details": str(e)}), 500

# Route to get all adverts (Public access)
@adverts_bp.route('/all', methods=['GET'])
def get_all_adverts():
    try:
        adverts = Advert.query.order_by(Advert.created_at.desc()).all()  # Match news sorting
        return jsonify([advert.to_dict() for advert in adverts]), 200
    except Exception as e:
        return jsonify({"error": "Error occurred", "details": str(e)}), 500

# Route to get a single advert by ID (Public access)
@adverts_bp.route('/advert/<int:id>', methods=['GET'])
def get_advert(id):
    try:
        advert = Advert.query.get(id)
        if not advert:
            return jsonify({"error": "Advert not found"}), 404
        return jsonify(advert.to_dict()), 200
    except Exception as e:
        return jsonify({"error": "Error occurred", "details": str(e)}), 500

# Route to update an advert (Admin access required)
@adverts_bp.route('/update/<int:id>', methods=['PUT'])
@jwt_required()
def update_advert(id):
    try:
        current_user = get_jwt_identity()
        advert = Advert.query.get(id)
        if not advert:
            return jsonify({"error": "Advert not found"}), 404

        # Check if it's a form submission with file or a JSON request
        if request.content_type and 'multipart/form-data' in request.content_type:
            # Handle form data with possible file upload
            if 'title' in request.form:
                advert.title = request.form.get('title')
            if 'description' in request.form:
                advert.description = request.form.get('description')
            if 'expires_at' in request.form:
                expires_at = request.form.get('expires_at')
                advert.expires_at = datetime.strptime(expires_at, "%Y-%m-%d %H:%M:%S") if expires_at else None

            # Handle image upload if present (optional)
            if 'image' in request.files:
                file = request.files['image']
                if file and allowed_file(file.filename):
                    # Delete old image if it exists
                    if advert.image_url and os.path.exists(os.path.join(UPLOAD_FOLDER, advert.image_url)):
                        os.remove(os.path.join(UPLOAD_FOLDER, advert.image_url))

                    filename = secure_filename(file.filename)
                    file_path = os.path.join(UPLOAD_FOLDER, filename)
                    file.save(file_path)
                    advert.image_url = filename
        else:
            # Handle JSON data without file
            data = request.get_json()
            advert.title = data.get('title', advert.title)
            advert.description = data.get('description', advert.description)
            advert.image_url = data.get('image_url', advert.image_url)
            if data.get('expires_at'):
                advert.expires_at = datetime.strptime(data.get('expires_at'), "%Y-%m-%d %H:%M:%S")

        db.session.commit()
        return jsonify(advert.to_dict()), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": "Error occurred", "details": str(e)}), 500

# Route to delete an advert (Admin access required)
@adverts_bp.route('/delete/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_advert(id):
    try:
        current_user = get_jwt_identity()
        advert = Advert.query.get(id)
        if not advert:
            return jsonify({"error": "Advert not found"}), 404

        # Delete the image file if it exists
        if advert.image_url and os.path.exists(os.path.join(UPLOAD_FOLDER, advert.image_url)):
            os.remove(os.path.join(UPLOAD_FOLDER, advert.image_url))

        db.session.delete(advert)
        db.session.commit()
        return jsonify({"message": "Advert deleted successfully"}), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": "Error occurred", "details": str(e)}), 500