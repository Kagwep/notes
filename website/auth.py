from flask import Blueprint,render_template,request,flash,redirect,url_for
from flask_login import login_user,logout_user,login_required
from werkzeug.security import generate_password_hash, check_password_hash
from .auth_manager import User
from .note import mysql,login_manager



auth = Blueprint('auth',__name__)

@login_manager.user_loader
def load_user(user_id):
        return User(user_id)  # Create a User object with the retrieved user ID


@auth.route('/login',methods=['GET','POST'])
def login():
    if request.method == 'POST':
        cur = mysql.connection.cursor()
        data = request.form
        email = data.get('email')
        password = data.get('password')
        
 
        # cur.execute("SELECT id FROM users WHERE email = %s AND password = %s", (email, password))
        
        cur.execute("SELECT * FROM user WHERE email = %s", (email,))
        
        user = cur.fetchone()
        print(user)
        
        if user:
            
            if check_password_hash(user[2],password):
                cur.close()
                user_id = user[0]
                login_user(user_id, remember=True)  
                flash('welcome back!',category='success')
                return redirect(url_for('views.home'))
            else:
              flash('The password is incorrect. please try again.',category='error')  
                
        else:
            flash('no user with those credentials was found.',category='error')
        
    return render_template("login.html",text="ve")



@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))


@auth.route('/signup',methods=['GET','POST'])
def signup():
    if request.method == 'POST':
        cur = mysql.connection.cursor()
        data = request.form
        email = data.get('email')
        name = data.get('name')
        password1 = data.get('password1')
        password2 = data.get('password2')

        cur.execute("SELECT * FROM user WHERE email = %s", (email,))
        
        user = cur.fetchone()
        
        if user:
            flash(f'User with email: {email} already exists.',category='error')
            
        elif len(email)<4:
            flash('Email must be grater than 4 charachters.',category='error')

        elif len(name) <2:
            flash('Name must be grater than 2 charachters.',category='error')
            
        elif password1 != password2:
            flash('Passwords dnt\'t match.',category='error')
            
        elif len(password1) < 4:
            flash('Password too short. password must be more that 4 charachters.',category='error')
        
        else:
            password = generate_password_hash(password1, method='sha256')
            cur.execute("INSERT INTO user (email,password,name) VALUES (%s,%s,%s)",(email,password,name))
            mysql.connection.commit()
            cur.close()
            user_id = user[0]
            login_user(user_id, remember=True) 
            flash('Account created!.',category='success')
            return redirect(url_for('views.home')) 
            
                              
    return render_template('signup.html')