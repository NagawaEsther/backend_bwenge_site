from flask import Blueprint, request, jsonify
from bwenge_app.models.Subscription import Subscribe
from bwenge_app import db

subscribe_bp = Blueprint('subscribe', __name__, url_prefix='/api/v1/subscribe')

# Get all subscriptions
@subscribe_bp.route('/all', methods=['GET'])
def get_all_subscriptions():
    subscriptions = Subscribe.query.all()
    output = [{'id': sub.id, 'email': sub.email, 'subscribed_at': sub.subscribed_at} for sub in subscriptions]
    return jsonify({'subscriptions': output}), 200

# Subscribe a user
@subscribe_bp.route('/create', methods=['POST'])
def create_subscription():
    data = request.get_json()
    if 'email' not in data:
        return jsonify({'error': 'Email is required'}), 400

    new_subscription = Subscribe(email=data['email'])
    db.session.add(new_subscription)
    db.session.commit()
    return jsonify({'message': 'Subscription created successfully', 'subscription': {'id': new_subscription.id, 'email': new_subscription.email}}), 201

# Update a subscription
@subscribe_bp.route('/update/<int:id>', methods=['PUT'])
def update_subscription(id):
    subscription = Subscribe.query.get_or_404(id)
    data = request.get_json()

    if 'email' in data:
        subscription.email = data['email']

    db.session.commit()
    return jsonify({'message': 'Subscription updated successfully', 'subscription': {'id': subscription.id, 'email': subscription.email}}), 200

# Delete a subscription
@subscribe_bp.route('/delete<int:id>', methods=['DELETE'])
def delete_subscription(id):
    subscription = Subscribe.query.get_or_404(id)
    db.session.delete(subscription)
    db.session.commit()
    return jsonify({'message': 'Subscription deleted successfully'}), 200
