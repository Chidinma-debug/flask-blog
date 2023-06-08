import os   # module used to grab extention of uploaded file of profile pic
import secrets
from PIL import Image #resize uploaded images 
from flask import url_for
from flaskblog import app, mail
from flask_mail import Message

def save_picture(form_picture):
    #save new profile picture
    random_hex = secrets.token_hex(8)
#this os.path...function returns file name without extension and extension name. form_pic is submitted picture
#usually its f_name, f_ext = os.path.... but replace f_name with _ because we dont need it. only extension is needed
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext  #gives pic a new filename of secretkey+extension
    #create path where updated image will be stored. Read more about os module
    picture_path = os.path.join(app.root_path, 'static/profile_pics', picture_fn)
    #resize images to 125px
    output_size = (125, 125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path) #save new picture in created path
    return picture_fn
    
#define a function to send reset email
def send_reset_email(user):
    token = user.get_reset_token()
    msg = Message('Password Reset Request', sender='noreply@demo.com', recipients=[user.email])
    msg.body = f'''To reset your password, visit the following link:
{url_for('users.reset_token', token=token, _external=True)}
If you did not make this request then simply ignore this email and no changes will be made
'''
    mail.send(msg)
