from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from bwenge_app.extensions import db,bcrypt
from bwenge_app.extensions import migrate
from flask_jwt_extended import JWTManager
from flask_jwt_extended import JWTManager, jwt_required, get_jwt_identity
from flask import Flask, jsonify, send_from_directory
from flask_swagger_ui import get_swaggerui_blueprint
from flask import send_from_directory
import os  
from flask_cors import CORS

#importing bluebrints
from bwenge_app.controllers.admin_controller import admin_bp
from bwenge_app.controllers.adverts_controller import adverts_bp
from bwenge_app.controllers.contact_controller import contact_bp
from bwenge_app.controllers.news_controller import news_bp
from bwenge_app.controllers.subscriptions_controller import subscribe_bp

def create_app():
    app = Flask(__name__)
    CORS(app)
    app.config.from_object('config.Config')
    app.config['UPLOAD_FOLDER'] = 'static/uploads'  # Match the UPLOAD_FOLDER in the controller

    # Initialize database
    db.init_app(app)
    migrate.init_app(app,db)
    bcrypt.init_app(app)

    # Initialize JWTManager with secret key
    app.config['JWT_SECRET_KEY'] = '12345'  
    jwt = JWTManager(app)



    # Configure token expiration time 
    app.config['JWT_ACCESS_TOKEN_EXPIRES'] = 3600  


    #importing models

    from bwenge_app.models.admin import Admin
    from bwenge_app.models.contact import Contact
    from bwenge_app.models.news import News
    from bwenge_app.models.adverts import Advert
    from bwenge_app.models.Subscription import Subscribe
  
    


    # Register blueprints
    
    app.register_blueprint(admin_bp,url_prefix='/api/v1/auth')
    app.register_blueprint(adverts_bp,url_prefix='/api/v1/adverts')
    app.register_blueprint(contact_bp,url_prefix='/api/v1/contact')
    app.register_blueprint(news_bp,url_prefix='/api/v1/news')
    app.register_blueprint(subscribe_bp,url_prefix='/api/v1/subscribe')


    # Serve Swagger JSON file
    @app.route('/swagger.json')
    def serve_swagger_json():
        try:
            return send_from_directory(os.path.dirname(os.path.abspath(__file__)), 'swagger.json')

        except FileNotFoundError:
            return jsonify({"message": "Swagger JSON file not found"}), 404
        
    # Swagger UI configuration
    SWAGGER_URL = '/api/docs'  
    API_URL = '/swagger.json'  
    
    # Create Swagger UI blueprint
    swaggerui_blueprint = get_swaggerui_blueprint(
        SWAGGER_URL,
        API_URL,
        config={  
            'app_name': "Bwenge_app"
        }
    )
    
    # Register Swagger UI blueprint
    app.register_blueprint(swaggerui_blueprint)


    @app.route('/')
    def home():
        return 'Welcome to Bwenge app!'
    
    # Routes for protected resources
    @app.route('/protected')
    @jwt_required()
    def protected():
        current_user_id = get_jwt_identity()
        return jsonify(logged_in_as=current_user_id), 200


    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
