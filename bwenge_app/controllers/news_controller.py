from flask import Blueprint, request, jsonify, send_from_directory
from flask_jwt_extended import jwt_required, get_jwt_identity
from werkzeug.utils import secure_filename
import os
from bwenge_app.extensions import db
from bwenge_app.models.news import News

news_bp = Blueprint('news', __name__, url_prefix='/api/v1/news')

# Configure upload folder and allowed extensions
UPLOAD_FOLDER = r'C:\news\images'  # Match RhemaBlog's dedicated folder approach
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}  # Match RhemaBlog's allowed extensions

# Ensure the upload folder exists
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Route to serve images
@news_bp.route('/images/<filename>', methods=['GET'])
def serve_image(filename):
    return send_from_directory(UPLOAD_FOLDER, filename)

# Route to create a news item (Admin access required)
@news_bp.route('/news', methods=['POST'])

def create_news():
    try:
        # Check if it's a form submission with file or a JSON request
        if request.content_type and 'multipart/form-data' in request.content_type:
            # Handle form data with file upload
            title = request.form.get('title')
            content = request.form.get('content')
            
            if not title or not content:
                return jsonify({"error": "Title and content are required"}), 400
            
            # Handle image upload if present (optional)
            image_filename = None
            if 'image' in request.files:
                file = request.files['image']
                if file and allowed_file(file.filename):
                    filename = secure_filename(file.filename)
                    file_path = os.path.join(UPLOAD_FOLDER, filename)
                    file.save(file_path)
                    image_filename = filename
            
            # Create a new News instance
            news_item = News(
                title=title,
                content=content,
                image_url=image_filename  # Store only the filename
            )
        else:
            # Handle JSON data without file
            data = request.get_json()
            if not data.get('title') or not data.get('content'):
                return jsonify({"error": "Title and content are required"}), 400
            
            news_item = News(
                title=data.get('title'),
                content=data.get('content'),
                image_url=data.get('image_url')  # Allow external URL
            )

        db.session.add(news_item)
        db.session.commit()

        return jsonify({
            "message": "News created successfully",
            "id": news_item.id,
            "image_url": news_item.image_url
        }), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": "Error occurred", "details": str(e)}), 500

# Route to update a news item (Admin access required)
@news_bp.route('/news/<int:id>', methods=['PUT'])

def update_news(id):
    try:
        news_item = News.query.get(id)
        if not news_item:
            return jsonify({"error": "News article not found"}), 404

        # Check if it's a form submission with file or a JSON request
        if request.content_type and 'multipart/form-data' in request.content_type:
            # Handle form data with possible file upload
            if 'title' in request.form:
                news_item.title = request.form.get('title')
            if 'content' in request.form:
                news_item.content = request.form.get('content')
            
            # Handle image upload if present (optional)
            if 'image' in request.files:
                file = request.files['image']
                if file and allowed_file(file.filename):
                    # Delete old image if it exists
                    if news_item.image_url and os.path.exists(os.path.join(UPLOAD_FOLDER, news_item.image_url)):
                        os.remove(os.path.join(UPLOAD_FOLDER, news_item.image_url))
                    
                    filename = secure_filename(file.filename)
                    file_path = os.path.join(UPLOAD_FOLDER, filename)
                    file.save(file_path)
                    news_item.image_url = filename
        else:
            # Handle JSON data without file
            data = request.get_json()
            news_item.title = data.get('title', news_item.title)
            news_item.content = data.get('content', news_item.content)
            news_item.image_url = data.get('image_url', news_item.image_url)

        db.session.commit()
        return jsonify(news_item.to_dict()), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": "Error occurred", "details": str(e)}), 500

# Route to get all news items (Public access)
@news_bp.route('/news', methods=['GET'])
def get_all_news():
    try:
        news_items = News.query.order_by(News.created_at.desc()).all()  # Match RhemaBlog's sorting
        return jsonify([news_item.to_dict() for news_item in news_items]), 200
    except Exception as e:
        return jsonify({"error": "Error occurred", "details": str(e)}), 500

# Route to get a single news item by ID (Public access)
@news_bp.route('/news/<int:id>', methods=['GET'])
def get_news(id):
    try:
        news_item = News.query.get(id)
        if not news_item:
            return jsonify({"error": "News article not found"}), 404
        return jsonify(news_item.to_dict()), 200
    except Exception as e:
        return jsonify({"error": "Error occurred", "details": str(e)}), 500

# Route to delete a news item (Admin access required)
@news_bp.route('/news/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_news(id):
    try:
        news_item = News.query.get(id)
        if not news_item:
            return jsonify({"error": "News article not found"}), 404

        # Delete the image file if it exists
        if news_item.image_url and os.path.exists(os.path.join(UPLOAD_FOLDER, news_item.image_url)):
            os.remove(os.path.join(UPLOAD_FOLDER, news_item.image_url))

        db.session.delete(news_item)
        db.session.commit()
        return jsonify({"message": "News article deleted successfully"}), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": "Error occurred", "details": str(e)}), 500