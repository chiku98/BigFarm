import pymysql 
from flask import Flask, flash,jsonify, render_template, session,redirect,request,url_for
import re
from werkzeug.security import generate_password_hash,check_password_hash
from flask_cors import CORS,cross_origin
from flaskext.mysql import MySQL
from werkzeug.utils import secure_filename
import os


app=Flask(__name__)
CORS(app)

app.config['SECRET_KEY'] = 'secret-key'

app.config.from_pyfile('config.py')


mysql = MySQL()

mysql.init_app(app)

conn = mysql.connect()
cursor = conn.cursor(pymysql.cursors.DictCursor)


UPLOAD_FOLDER = 'static/uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
# app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif','mp4'])


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def Landing_page():
    return render_template('Landing_page.html')
@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/signup')
def signup():
    return render_template('register.html')

@app.route('/details')
def details():
    return render_template('details.html')
@app.route('/home')
def home ():
     return render_template('home.html')

@app.route('/help')
def  help():
    return render_template('help.html')   


@app.route('/property')
def property():
    return render_template('property.html')   

@app.route('/profiledetails')
def profiledetails():
    return render_template('profiledetails.html') 


@app.route('/register', methods=['POST'])
def register():
    if request.method == 'POST':
        msg = ''

    # Check if "email", "password" POST requests exist (user submitted form)
    if request.method == 'POST' and 'name' in request.form and 'email' in request.form and 'mobile' in request.form and 'password' in request.form:
        # Create variables for easy access
        name = request.form['name']
        email = request.form['email']
        mobile = request.form['mobile']
        password = request.form['password']
        confirm_password = request.form['confirm_password']

        # Check if account exists using MySQL
        cursor.execute('SELECT * FROM user WHERE email = %s', (email))
        account = cursor.fetchone()
        # If account exists show error and validation checks
        if account:
            msg = 'Account already exists! Please log in'
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            msg = 'Invalid email address!'
            return render_template("register.html", msg=msg)
        elif len(password) <= 6 and re.match(r'[A-Za-z0-9^@]+', password):
            msg = 'password minimum 6 characters and must contain one upper case letter,special character and numbers!'
            return render_template("register.html", msg=msg)
        elif confirm_password != password:
            msg = "password doesn't match"
            return render_template("register.html", msg=msg)
        elif not email or not password or not name or not confirm_password:
            msg = 'Please fill out the form!'
            return render_template("register.html", msg=msg)
        
        elif email and password and confirm_password :

            cursor.execute('INSERT INTO user (name, email, mobile, password, confirm_password) VALUES (%s, %s, %s, %s, %s)',
                           (name, email, mobile, password, confirm_password))
            conn.commit()
            msg = 'Successfully registered. Login To Continue'

            return redirect('login')
        else:
            msg = 'Wrong Crenditals'

    return render_template('Landing_page.html')
                       
@app.route('/login',methods=['GET','POST'])
def login():
    msg = ''
    # Check if "email" and "password" POST requests exist (user submitted form)
    if request.method == 'POST' and 'email' in request.form and 'password' in request.form:
        # Create variables for easy access
        email = request.form['email']
        password = request.form['password']
        # Check if account exists using MySQL
        cursor.execute(
            'SELECT * FROM user WHERE email = %s AND password = %s', (email, password))
        # Fetch one record and return result
        account = cursor.fetchone()

        # If account exists in accounts table in out database
        if account:
            # Create session data, we can access this data in other routes
            session['loggedin'] = True
            session['email'] = account['email']
            # Redirect to home page
            # return 'Logged in successfully!'
            msg='Successfully Loggedin.'
            return redirect(url_for('home'))
        else:
            # Account doesnt exist or email/password incorrect
            msg = 'Incorrect email/password!'
    return render_template('login.html',msg=msg)

#Seller Data

@app.route('/ads',methods=['GET','POST'])
def ads():
    if request.method == 'POST':
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        mobile_no = request.form['mobile_no']
        email = request.form['email']
        property_details = request.form['property_details']
        price = request.form['price']
        address= request.form['address']
        description= request.form['description']
        cursor.execute("INSERT INTO seller(first_name,last_name,mobile_no,email,property_details,price,address,description) VALUES(%s,%s,%s,%s,%s,%s,%s,%s) ",(first_name,last_name,mobile_no,email,property_details,price,address,description) )
        if request.method == 'POST':
                photo = request.files.getlist('photo[]')
                for file in photo :
                    if file and allowed_file(file.filename):
                        filename = secure_filename(file.filename)
                        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                        cursor.execute("UPDATE seller SET photo=%s WHERE email=%s", [filename,email])
                        cursor.fetchone()
        if request.method == 'POST':
                video = request.files.getlist('video[]')
                for file in video:
                    if file and allowed_file(file.filename):
                        filename = secure_filename(file.filename)
                        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                        cursor.execute("UPDATE seller SET video=%s WHERE email=%s", [filename,email])
                        cursor.fetchone()
        conn.commit()
        return redirect('home')        
    return render_template('home.html')


@app.route('/profile')
def profile():
    return render_template('profile.html')

@app.route('/Profile', methods=['POST'])
def Profile():
    cursor = None
    conn = None
    try:
        conn = mysql.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        form = request.form
        email=form["email"]
        phone = form ["phone"]
        if email and phone and request.method=='POST':
           cursor.execute("UPDATE user SET email = %s, phone = %s WHERE id = %s",
            (email, phone, session['id'],))   
           conn.commit()
           response = render_template('profile.html')
           response.status_code=201
           return response     
    except Exception as e:
        print(e)
    finally:
        conn()
        cursor() 
if __name__ == '__main__':
    app.run(debug=True,port=5002)




