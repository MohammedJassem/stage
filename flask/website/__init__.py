from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
#from flask_socketio import socketIO,send ,recieve

#from SQLAlchemy.orm import relationship


"""from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView"""
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///website.db'
app.config['SECRET_KEY'] = '59a927673e2daf590de2d47a'
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
#socketio = socketIO(app)

login_manager = LoginManager(app)
#login_manager.login_view = "DeleteAdmin"
#login_manager.login_message_category = "info"
from website import routes


