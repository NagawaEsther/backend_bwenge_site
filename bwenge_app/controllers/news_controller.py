from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from bwenge_app.extensions import db

from functools import wraps

from bwenge_app.models.news import News

news_bp = Blueprint('news', __name__, url_prefix='/api/v1/news')


# Route to create a news item (Admin access required)
@news_bp.route('/news', methods=['POST'])

def create_news():
    data = request.get_json()
    title = data.get('title')
    content = data.get('content')
    image_url = data.get('image_url', None)

    news_item = News(title=title, content=content, image_url=image_url)
    db.session.add(news_item)
    db.session.commit()
    
    return jsonify(news_item.to_dict()), 201

# Route to get all news items (Public access)
@news_bp.route('/news', methods=['GET'])
def get_all_news():
    news = News.query.all()
    return jsonify([news_item.to_dict() for news_item in news]), 200

# Route to get a single news item by ID (Public access)
@news_bp.route('/news/<int:id>', methods=['GET'])
def get_news(id):
    news_item = News.query.get_or_404(id)
    return jsonify(news_item.to_dict()), 200

# Route to update a news item (Admin access required)
@news_bp.route('/news/<int:id>', methods=['PUT'])

def update_news(id):
    news_item = News.query.get_or_404(id)
    data = request.get_json()

    news_item.title = data.get('title', news_item.title)
    news_item.content = data.get('content', news_item.content)
    news_item.image_url = data.get('image_url', news_item.image_url)

    db.session.commit()
    return jsonify(news_item.to_dict()), 200

# Route to delete a news item (Admin access required)
@news_bp.route('/news/<int:id>', methods=['DELETE'])
def delete_news(id):
    news_item = News.query.get_or_404(id)
    db.session.delete(news_item)
    db.session.commit()
    return jsonify({"message": "News item deleted"}), 200
