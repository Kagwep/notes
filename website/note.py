from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_mysqldb import MySQL
from flask_login import LoginManager

login_manager = LoginManager()


app= Flask(__name__)
app.config['SECRET_KEY'] = 'gweygakefguiak cjoagwdoa'
app.config['MYSQL_USER'] = "root"
app.config['MYSQL_PASSWORD'] = "@kagwe2023&"
app.config['MYSQL_DB'] = "notesdb"

mysql = MySQL(app)

login_manager.login_view = 'auth.login'
login_manager.init_app(app)

@login_manager.user_loader
def load_user(id):

    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM user WHERE id = %s", (int(id),))
    user = cur.fetchone()

    return user
    


from .views import views
from .auth  import auth


app.register_blueprint(views,url_prefix='/')
app.register_blueprint(auth,url_prefix='/')


app = app
    
    


    