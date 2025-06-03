# # from flask import Blueprint, request, jsonify
# # from flask_jwt_extended import jwt_required, get_jwt_identity
# # from bwenge_app.extensions import db

# # from functools import wraps

# # from bwenge_app.models.news import News

# # news_bp = Blueprint('news', __name__, url_prefix='/api/v1/news')


# # # Route to create a news item (Admin access required)
# # @news_bp.route('/news', methods=['POST'])

# # def create_news():
# #     data = request.get_json()
# #     title = data.get('title')
# #     content = data.get('content')
# #     image_url = data.get('image_url', None)

# #     news_item = News(title=title, content=content, image_url=image_url)
# #     db.session.add(news_item)
# #     db.session.commit()
    
# #     return jsonify(news_item.to_dict()), 201

# # # Route to get all news items (Public access)
# # @news_bp.route('/news', methods=['GET'])
# # def get_all_news():
# #     news = News.query.all()
# #     return jsonify([news_item.to_dict() for news_item in news]), 200

# # # Route to get a single news item by ID (Public access)
# # @news_bp.route('/news/<int:id>', methods=['GET'])
# # def get_news(id):
# #     news_item = News.query.get_or_404(id)
# #     return jsonify(news_item.to_dict()), 200

# # # Route to update a news item (Admin access required)
# # @news_bp.route('/news/<int:id>', methods=['PUT'])

# # def update_news(id):
# #     news_item = News.query.get_or_404(id)
# #     data = request.get_json()

# #     news_item.title = data.get('title', news_item.title)
# #     news_item.content = data.get('content', news_item.content)
# #     news_item.image_url = data.get('image_url', news_item.image_url)

# #     db.session.commit()
# #     return jsonify(news_item.to_dict()), 200

# # # Route to delete a news item (Admin access required)
# # @news_bp.route('/news/<int:id>', methods=['DELETE'])
# # def delete_news(id):
# #     news_item = News.query.get_or_404(id)
# #     db.session.delete(news_item)
# #     db.session.commit()
# #     return jsonify({"message": "News item deleted"}), 200


# # from flask import Blueprint, request, jsonify, send_from_directory
# # from flask_jwt_extended import jwt_required, get_jwt_identity
# # from werkzeug.utils import secure_filename
# # import os
# # from bwenge_app.extensions import db
# # from bwenge_app.models.news import News

# # # Create Blueprint for News routes
# # news_bp = Blueprint('news', __name__, url_prefix='/api/v1/news')

# # UPLOAD_FOLDER = r'C:\bwenge\news_images'
# # ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

# # # Create the upload folder if it doesn't exist
# # os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# # def allowed_file(filename):
# #     return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# # @news_bp.route('/images/<filename>', methods=['GET'])
# # def serve_image(filename):
# #     return send_from_directory(UPLOAD_FOLDER, filename)

# # # Route to create a news item (Admin access required)
# # @news_bp.route('/news', methods=['POST'])
# # @jwt_required()
# # def create_news():
# #     try:
# #         # Verify admin access
# #         current_user = get_jwt_identity()
# #         # Assuming admin check is handled in your authentication logic
        
# #         # Check if it's a form submission with file or a JSON request
# #         if request.content_type and 'multipart/form-data' in request.content_type:
# #             # Handle form data with file upload
# #             title = request.form.get('title')
# #             content = request.form.get('content')
            
# #             if not title or not content:
# #                 return jsonify({"message": "Title and content are required"}), 400
            
# #             # Handle image upload if present
# #             image_filename = None
# #             if 'image' in request.files:
# #                 file = request.files['image']
# #                 if file and allowed_file(file.filename):
# #                     filename = secure_filename(file.filename)
# #                     filepath = os.path.join(UPLOAD_FOLDER, filename)
# #                     file.save(filepath)
# #                     image_filename = filename
            
# #             # Create a new News instance
# #             news_item = News(
# #                 title=title,
# #                 content=content,
# #                 image_url=image_filename  # Store just the filename
# #             )
# #         else:
# #             # Handle JSON data without file
# #             data = request.get_json()
# #             if not data.get('title') or not data.get('content'):
# #                 return jsonify({"message": "Title and content are required"}), 400
            
# #             news_item = News(
# #                 title=data.get('title'),
# #                 content=data.get('content'),
# #                 image_url=data.get('image_url')  # This would be a URL or null
# #             )

# #         # Add to the session and commit to save it
# #         db.session.add(news_item)
# #         db.session.commit()

# #         return jsonify(news_item.to_dict()), 201

# #     except Exception as e:
# #         db.session.rollback()  # Rollback in case of error
# #         return jsonify({"message": "Error occurred", "error": str(e)}), 500

# # # Route to get all news items (Public access)
# # @news_bp.route('/news', methods=['GET'])
# # def get_all_news():
# #     try:
# #         news = News.query.all()
# #         return jsonify([news_item.to_dict() for news_item in news]), 200
# #     except Exception as e:
# #         return jsonify({"message": "Error occurred", "error": str(e)}), 500

# # # Route to get a single news item by ID (Public access)
# # @news_bp.route('/news/<int:id>', methods=['GET'])
# # def get_news(id):
# #     try:
# #         news_item = News.query.get_or_404(id)
# #         return jsonify(news_item.to_dict()), 200
# #     except Exception as e:
# #         return jsonify({"message": "Error occurred", "error": str(e)}), 500

# # # Route to update a news item (Admin access required)
# # @news_bp.route('/news/<int:id>', methods=['PUT'])
# # @jwt_required()
# # def update_news(id):
# #     try:
# #         # Verify admin access
# #         current_user = get_jwt_identity()
# #         # Assuming admin check is handled in your authentication logic

# #         news_item = News.query.get_or_404(id)

# #         # Check if it's a form submission with file or a JSON request
# #         if request.content_type and 'multipart/form-data' in request.content_type:
# #             # Handle form data with possible file upload
# #             if 'title' in request.form:
# #                 news_item.title = request.form.get('title')
# #             if 'content' in request.form:
# #                 news_item.content = request.form.get('content')
            
# #             # Handle image upload if present
# #             if 'image' in request.files:
# #                 file = request.files['image']
# #                 if file and allowed_file(file.filename):
# #                     # Delete old image if it exists
# #                     if news_item.image_url and os.path.exists(os.path.join(UPLOAD_FOLDER, news_item.image_url)):
# #                         os.remove(os.path.join(UPLOAD_FOLDER, news_item.image_url))
                    
# #                     filename = secure_filename(file.filename)
# #                     filepath = os.path.join(UPLOAD_FOLDER, filename)
# #                     file.save(filepath)
# #                     news_item.image_url = filename
# #         else:
# #             # Handle JSON data without file
# #             data = request.get_json()
# #             news_item.title = data.get('title', news_item.title)
# #             news_item.content = data.get('content', news_item.content)
# #             news_item.image_url = data.get('image_url', news_item.image_url)

# #         # Commit changes to the database
# #         db.session.commit()

# #         return jsonify(news_item.to_dict()), 200

# #     except Exception as e:
# #         db.session.rollback()  # Rollback in case of error
# #         return jsonify({"message": "Error occurred", "error": str(e)}), 500

# # # Route to delete a news item (Admin access required)
# # @news_bp.route('/news/<int:id>', methods=['DELETE'])
# # @jwt_required()
# # def delete_news(id):
# #     try:
# #         # Verify admin access
# #         current_user = get_jwt_identity()
# #         # Assuming admin check is handled in your authentication logic

# #         news_item = News.query.get_or_404(id)

# #         # Delete the image file if it exists
# #         if news_item.image_url:
# #             file_path = os.path.join(UPLOAD_FOLDER, news_item.image_url)
# #             if os.path.exists(file_path):
# #                 os.remove(file_path)

# #         # Delete the news item
# #         db.session.delete(news_item)
# #         db.session.commit()

# #         return jsonify({"message": "News item deleted successfully"}), 200

# #     except Exception as e:
# #         db.session.rollback()  # Rollback in case of error
# #         return jsonify({"message": "Error occurred", "error": str(e)}), 500

# from flask import Blueprint, request, jsonify, send_from_directory, current_app
# from flask_jwt_extended import jwt_required, get_jwt_identity
# from werkzeug.utils import secure_filename
# import os
# from bwenge_app.extensions import db
# from bwenge_app.models.news import News

# news_bp = Blueprint('news', __name__, url_prefix='/api/v1/news')

# UPLOAD_FOLDER = r'C:\bwenge\news_images'
# ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

# os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# def allowed_file(filename):
#     return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# # Middleware to log every request coming to this blueprint
# @news_bp.before_app_request
# def log_request_info():
#     print(f"REQUEST TO: {request.path}")
#     print(f"METHOD: {request.method}")
#     print(f"HEADERS: {dict(request.headers)}")
#     print(f"FORM DATA: {request.form}")
#     print(f"FILES: {request.files}")
#     try:
#         print(f"JSON DATA: {request.get_json(silent=True)}")
#     except Exception as e:
#         print(f"JSON parse error: {e}")

# @news_bp.route('/images/<filename>', methods=['GET'])
# def serve_image(filename):
#     print(f"Serving image: {filename}")
#     return send_from_directory(UPLOAD_FOLDER, filename)

# @news_bp.route('/news', methods=['POST'])
# @jwt_required()
# def create_news():
#     print("Create news route hit")
#     try:
#         current_user = get_jwt_identity()
#         print(f"Current user from JWT: {current_user}")

#         if request.content_type and 'multipart/form-data' in request.content_type:
#             print("Handling multipart/form-data request")
#             title = request.form.get('title')
#             content = request.form.get('content')
#             print(f"Title: {title}, Content: {content}")

#             if not title or not content:
#                 print("Missing title or content")
#                 return jsonify({"message": "Title and content are required"}), 400

#             image_filename = None
#             if 'image' in request.files:
#                 file = request.files['image']
#                 print(f"Received file: {file.filename}")
#                 if file and allowed_file(file.filename):
#                     filename = secure_filename(file.filename)
#                     filepath = os.path.join(UPLOAD_FOLDER, filename)
#                     file.save(filepath)
#                     print(f"Saved image to: {filepath}")
#                     image_filename = filename

#             news_item = News(title=title, content=content, image_url=image_filename)

#         else:
#             print("Handling JSON request")
#             data = request.get_json()
#             print(f"JSON data: {data}")
#             if not data or not data.get('title') or not data.get('content'):
#                 print("Missing title or content in JSON")
#                 return jsonify({"message": "Title and content are required"}), 400

#             news_item = News(
#                 title=data.get('title'),
#                 content=data.get('content'),
#                 image_url=data.get('image_url')
#             )

#         db.session.add(news_item)
#         db.session.commit()
#         print("News item created successfully")
#         return jsonify(news_item.to_dict()), 201

#     except Exception as e:
#         db.session.rollback()
#         print(f"Exception in create_news: {e}")
#         return jsonify({"message": "Error occurred", "error": str(e)}), 500

# @news_bp.route('/news', methods=['GET'])
# def get_all_news():
#     print("Get all news route hit")
#     try:
#         news = News.query.all()
#         print(f"Found {len(news)} news items")
#         return jsonify([news_item.to_dict() for news_item in news]), 200
#     except Exception as e:
#         print(f"Exception in get_all_news: {e}")
#         return jsonify({"message": "Error occurred", "error": str(e)}), 500

# @news_bp.route('/news/<int:id>', methods=['GET'])
# def get_news(id):
#     print(f"Get news by ID route hit: {id}")
#     try:
#         news_item = News.query.get_or_404(id)
#         return jsonify(news_item.to_dict()), 200
#     except Exception as e:
#         print(f"Exception in get_news: {e}")
#         return jsonify({"message": "Error occurred", "error": str(e)}), 500

# @news_bp.route('/news/<int:id>', methods=['PUT'])
# @jwt_required()
# def update_news(id):
#     print(f"Update news route hit for ID: {id}")
#     try:
#         current_user = get_jwt_identity()
#         print(f"Current user from JWT: {current_user}")

#         news_item = News.query.get_or_404(id)

#         if request.content_type and 'multipart/form-data' in request.content_type:
#             print("Handling multipart/form-data update")
#             if 'title' in request.form:
#                 news_item.title = request.form.get('title')
#                 print(f"Updated title to: {news_item.title}")
#             if 'content' in request.form:
#                 news_item.content = request.form.get('content')
#                 print(f"Updated content")

#             if 'image' in request.files:
#                 file = request.files['image']
#                 print(f"Received file for update: {file.filename}")
#                 if file and allowed_file(file.filename):
#                     if news_item.image_url:
#                         old_path = os.path.join(UPLOAD_FOLDER, news_item.image_url)
#                         if os.path.exists(old_path):
#                             os.remove(old_path)
#                             print(f"Deleted old image: {old_path}")

#                     filename = secure_filename(file.filename)
#                     filepath = os.path.join(UPLOAD_FOLDER, filename)
#                     file.save(filepath)
#                     news_item.image_url = filename
#                     print(f"Saved new image to: {filepath}")

#         else:
#             print("Handling JSON update")
#             data = request.get_json()
#             print(f"Update JSON data: {data}")
#             news_item.title = data.get('title', news_item.title)
#             news_item.content = data.get('content', news_item.content)
#             news_item.image_url = data.get('image_url', news_item.image_url)

#         db.session.commit()
#         print("News item updated successfully")
#         return jsonify(news_item.to_dict()), 200

#     except Exception as e:
#         db.session.rollback()
#         print(f"Exception in update_news: {e}")
#         return jsonify({"message": "Error occurred", "error": str(e)}), 500

# @news_bp.route('/news/<int:id>', methods=['DELETE'])
# @jwt_required()
# def delete_news(id):
#     print(f"Delete news route hit for ID: {id}")
#     try:
#         current_user = get_jwt_identity()
#         print(f"Current user from JWT: {current_user}")

#         news_item = News.query.get_or_404(id)

#         if news_item.image_url:
#             file_path = os.path.join(UPLOAD_FOLDER, news_item.image_url)
#             if os.path.exists(file_path):
#                 os.remove(file_path)
#                 print(f"Deleted image file: {file_path}")

#         db.session.delete(news_item)
#         db.session.commit()
#         print("News item deleted successfully")

#         return jsonify({"message": "News item deleted successfully"}), 200

#     except Exception as e:
#         db.session.rollback()
#         print(f"Exception in delete_news: {e}")
#         return jsonify({"message": "Error occurred", "error": str(e)}), 500


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
