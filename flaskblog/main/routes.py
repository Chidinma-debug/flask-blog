from flask import Blueprint
from flask import render_template, request
from flaskblog.models import Post
main = Blueprint('main', __name__)

#use main.route instead of app.route
@main.route("/")
@main.route("/home")
def home():
    #display all posts on home screen
    # posts = Post.query.all() is used to show all pages on home page. Paginate shows a particular number
    page = request.args.get('page', 1, type=int) #not needed for query.all
    posts = Post.query.order_by(Post.date.desc()).paginate(page=page, per_page=3) #3 posts per page. .order_by is only needed if you want to order
    return render_template('home.html', posts=posts)

@main.route("/about")
def about():
   return render_template('about.html')