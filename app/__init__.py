from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_mail import Mail
from config import Config
from datetime import datetime  # Import for now()

# Initialize extensions
db = SQLAlchemy()
login_manager = LoginManager()
login_manager.login_view = 'auth.login'
login_manager.login_message_category = 'info'
mail = Mail()

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Initialize extensions
    db.init_app(app)
    login_manager.init_app(app)
    mail.init_app(app)

    # Inject `now` globally for templates
    @app.context_processor
    def inject_now():
        return {'now': datetime.now()}

    # Register blueprints
    from app.routes.main import main
    from app.routes.auth import auth
    from app.routes.portfolio import portfolio

    app.register_blueprint(main)
    app.register_blueprint(auth)
    app.register_blueprint(portfolio)

    # Create database tables
    with app.app_context():
        db.create_all()

        # Initialize default data if needed
        from app.models import initialize_default_data
        initialize_default_data()

    return app
