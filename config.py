from flask import Flask, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from sqlalchemy import MetaData
from datetime import datetime
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from flask_admin.menu import MenuLink
import secrets

# Creates an instance of the blog application and defines any configuration details for it
app = Flask(__name__)

# SECRET KEY FOR FLASK FORMS
app.config['SECRET_KEY'] = secrets.token_hex(16)
# Flask applications require a secret key for securely signing the session cookie

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

# DATABASE ADMINISTRATOR
# Link in database admin page to the blog homepage for easy navigation
class MainIndexLink(MenuLink):
    def get_url(self):
        return url_for('index')

# Override ModelView class to state what data should be viewed from each table
class PostView(ModelView):
    column_display_pk = True
    column_hide_backrefs = True
    column_list = ('id', 'created', 'title', 'body')

# Create instance of admin class
admin = Admin(app, name='DB Admin', template_mode='bootstrap4')
# Remove link to db admin homepage
admin._menu = admin._menu[1:]
# Add link to blog homepage for easy navigation
admin.add_link(MainIndexLink(name='Home Page'))
# Add an instance of PostView class to the admin instance
admin.add_view(PostView(Post, db.session))

# IMPORT BLUEPRINTS
from accounts.views import accounts_bp
from posts.views import posts_bp
from security.views import security_bp

# REGISTER BLUEPRINTS
app.register_blueprint(accounts_bp)
app.register_blueprint(posts_bp)
app.register_blueprint(security_bp)