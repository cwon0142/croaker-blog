from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from sqlalchemy import MetaData
from datetime import datetime

# Creates an instance of the blog application and defines any configuration details for it
app = Flask(__name__)

# DATABASE CONFIGURATION
# Location of the database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///croakerblog.db'
# SQL commands will be output to the console
app.config['SQLALCHEMY_ECHO'] = True
# Removes the creation of a listener that sends a signal each time a change is made to the database
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Defines a naming convention for database columns
metadata = MetaData(
    naming_convention={
        "ix": 'ix_%(column_0_label)s',
        "uq": "uq_%(table_name)s_%(column_0_name)s",
        "ck": "ck_%(table_name)s_%(constraint_name)s",
        "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
        "pk": "pk_%(table_name)s"
    }
)

# Creates a database instance called db
db = SQLAlchemy(app, metadata=metadata)
# Initialises the use of migrations (database schema changes) by creating a Migrate isntance
migrate = Migrate(app, db)

# DATABASE TABLES
class Post(db.Model):
    __tablename__ = 'posts'

    id = db.Column(db.Integer, primary_key=True)
    created = db.Column(db.DateTime, nullable=False)
    title = db.Column(db.Text, nullable=False)
    body = db.Column(db.Text, nullable=False)

    def __init__(self, title, body):
        self.created = datetime.now()
        self.title = title
        self.body = body

# IMPORT BLUEPRINTS
from accounts.views import accounts_bp
from posts.views import posts_bp
from security.views import security_bp

# REGISTER BLUEPRINTS
app.register_blueprint(accounts_bp)
app.register_blueprint(posts_bp)
app.register_blueprint(security_bp)