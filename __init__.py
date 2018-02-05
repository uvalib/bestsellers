# This file is sort of like Handler.pm, it doesn't do anything except set up stuff for other parts to use
import logging, sys

from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.user import UserManager, SQLAlchemyAdapter
from flask.ext.mail import Mail

app = Flask(__name__)
app.config.from_object('bestsellers.config')

db = SQLAlchemy(app)

from bestsellers.models import User
from bestsellers.forms import password_validator

user_manager = UserManager(SQLAlchemyAdapter(db, User), password_validator=password_validator)
user_manager.init_app(app)

mail = Mail(app)

# This line needs to be here to force our app to load the urls from views
# In Apache it functions properly, but runserver doesn't load views unless you explicitly force it to.
from bestsellers import views
