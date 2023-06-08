from datetime import datetime
from itsdangerous import URLSafeSerializer as Serializer #password reset. itsdangrous is installed with flask
from flaskblog import db, login_manager, app
from flask_login import UserMixin

# this function below is with a decorator. Used to reload user from user Id. its necessary for loginManager to work
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

#Usermixin is a class in login manager that applies all required attributes
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    password = db.Column(db.String(60), nullable=False)
    # one user many posts. One to many relationship between user and posta
    posts = db.relationship('Post', backref='author', lazy=True) #Post is name of relationship class
    # backref means when you have a post, you can use the author attribute to get the user

#Lines 24-37 is used to reset password by sending user an email
#use serializer to pass in secretkey and expiration time
    def get_reset_token(self):
        s = Serializer(app.config['SECRET_KEY'],) #link to user's secret key
        return s.dumps({'user_id': self.id}).decode('utf-8')  #return token created by dump s method with secret key
        #decode to utf-8 or it will be in byte

#this function method verifies a token. Token my be invalid or time would have expired
    @staticmethod   #let python know that we wont be having self as an arguement, just token
    def verify_reset_token(token, expires_sec=1800):
        s = Serializer(app.config['SECRET_KEY'])
        try:
            user_id = s.loads(token, expires_sec)['user_id']
        except:
            return None
        return User.query.get(user_id)

# def __repr__ defines how objects are printed or returned
    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.image_file}')"


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    content = db.Column(db.Text, nullable=False)
    # state relationship here with foreign key. For foreign key, you are referencing the table not class, hence
    # user not User. Unlike in the defined relationship above. 
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f"User('{self.title}', '{self.date}')"
        # content may be too long and when looping through each post, title and date is enough
# Author isnt in post model because users will write posts so post and user model will have a relationship
# one to many relationship. One user, many posts