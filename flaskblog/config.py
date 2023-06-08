import os

#We need to set a secret key whcich will protect against modyfying cookies and forgery attacks so add app.config
#hide secret keys in environment variables instead of python script. control panel>systems and security
#>systems> Advanced settings> Add new environment variables> new user variables
#you should use SECRET_KEY='os.environ.get('SECRET_KEY')
#And SQLALCHEMY_DATABASE_URI=os.environ.get('SQLALCHEMY_DATABASE_URI') but ts not working for some reason

class Config:
    SECRET_KEY = '8fb3d5541452a3ac7fdfdefbe9ceed1d'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///site.db'
    MAIL_SERVER = 'smtp.googlemail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.environ.get('EMAIL_USER')
    MAIL_PASSWORD = os.environ.get('EMAIL_PASS')