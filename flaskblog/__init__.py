#  init.py initialize applicaion and bring together different components
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt  
from flask_login import LoginManager
from flask_mail import Mail    #send email
from flaskblog.config import Config
#Bycrypt hashes pasword in database

app = Flask(__name__)
app.config.from_object(Config)
#when db.create_all() is run in terminal. a site.db file is created
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'users.login'
#To make the error message finer when a user tries to access /account without loging in by directly putting it in the 
#browser. Use bootstrap attribute below
login_manager.login_message_category ='info'
#sending mail

mail = Mail(app)


#login used must be the function name of the route. all blueprints have different route names
from flaskblog.users.routes import users
from flaskblog.posts.routes import posts
from flaskblog.main.routes import main
from flaskblog.errors.handlers import errors

#register each blueprint
app.register_blueprint(users)
app.register_blueprint(posts)
app.register_blueprint(main)
app.register_blueprint(errors)