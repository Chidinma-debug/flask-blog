from flask import render_template, url_for, flash, redirect, request, abort, Blueprint
from flaskblog import db 
from flaskblog.posts.forms import PostForm
from flaskblog.models import Post
from flask_login import current_user, login_required 

posts = Blueprint('posts', __name__)
#change all @app.route to users. route...users is defined with blueprint above

@posts.route("/post/new", methods=['GET', 'POST'])
@login_required
def new_post():
    form = PostForm()
    if form.validate_on_submit():
        #Add new post to db. You can use id or current user for author
        post = Post(title=form.title.data, content=form.content.data, author=current_user)
        db.session.add(post)
        db.session.commit()
        flash('Your post has been created', 'success')
        return redirect(url_for('main.home'))
    return render_template('create_post.html', title='New Post', legend='Update Post', form=form)

# create a route to open a post by defining a function for each post
@posts.route("/post/<int:post_id>") #just viewing so no need for get or post request
def post(post_id):
    #you can use get method because its an id
    post = Post.query.get_or_404(post_id) #if post with that id doesnt exist, give a 404 error
    return render_template('post.html', title=post.title, post=post)

#route to update a post
@posts.route("/post/<int:post_id>/update", methods=['GET', 'POST'])
@login_required
def update_post(post_id):
    post = Post.query.get_or_404(post_id) #if post with that id doesnt exist, give a 404 error
    #only owners of post should be able to update it. use post.author to access user model
    if post.author != current_user:
        abort(403) #403 is http response for forbidden route
    form = PostForm()
    if form.validate_on_submit():
        post.title=form.title.data
        post.content=form.content.data
        db.session.commit()  #no need to add, post is already in the db
        flash('Your post has been Updated!', 'success')
        return redirect(url_for('posts.post', post_id=post.id))
    elif request.method =='GET':
    #UPDATE post on post page and home page
        form.title.data = post.title
        form.content.data = post.content
    return render_template('create_post.html', title='Update Post', legend='Update Post', form=form)

#Delete route: No get request 
@posts.route("/post/<int:post_id>/delete", methods=['POST'])
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id) #if post with that id doesnt exist, give a 404 error
    #only owners of post should be able to update it. To link post and user, use author i.e post.author
    if post.author != current_user:
        abort(403) #403 is http response for forbidden route
    db.session.delete(post)
    db.session.commit()
    flash('Your post has been Deleted!', 'success')
    return redirect(url_for('main.home'))
