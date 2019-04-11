#!/usr/bin/env python
#
# Project: Video Streaming with Flask
# Author: Log0 <im [dot] ckieric [at] gmail [dot] com>
# Date: 2014/12/21
# Website: http://www.chioka.in/
# Description:
# Modified to support streaming out with webcams, and not just raw JPEGs.
# Most of the code credits to Miguel Grinberg, except that I made a small tweak. Thanks!
# Credits: http://blog.miguelgrinberg.com/post/video-streaming-with-flask
#
# Usage:
# 1. Install Python dependencies: cv2, flask. (wish that pip install works like a charm)
# 2. Run "python main.py".
# 3. Navigate the browser to the local webpage.
from flask import Flask, render_template, Response, jsonify, redirect, request, url_for, flash,flash, session, abort
from camera import VideoCamera
from PIL import Image
import re
from io import BytesIO
import io
import base64
import secrets
from flask_sqlalchemy import sqlalchemy, SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash


# Change dbname here
db_name = "auth.db"
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///{db}'.format(db=db_name)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# SECRET_KEY required for session, flash and Flask Sqlalchemy to work
app.config['SECRET_KEY'] = 'ConfigureStrongSecretKeyHere'
db = SQLAlchemy(app)
camera =  VideoCamera()


class User(db.Model):
    uid = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    pass_hash = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        return '' % self.username

def create_db():
    """ # Execute this first time to create new db in current directory. """
    db.create_all()




@app.route("/signup/", methods=["GET", "POST"])
def signup():
    """
    Implements signup functionality. Allows username and password for new user.
    Hashes password with salt using werkzeug.security.
    Stores username and hashed password inside database.
    Username should to be unique else raises sqlalchemy.exc.IntegrityError.
    """

    if request.method == "POST":
        username = request.form['username']
        password = request.form['password']

        if not (username and password):
            flash("Username or Password cannot be empty")
            return redirect(url_for('signup'))
        else:
            username = username.strip()
            password = password.strip()

        # Returns salted pwd hash in format : method$salt$hashedvalue
        hashed_pwd = generate_password_hash(password, 'sha256')

        new_user = User(username=username, pass_hash=hashed_pwd)
        db.session.add(new_user)

        try:
            db.session.commit()
        except sqlalchemy.exc.IntegrityError:
            flash("Username {u} is not available.".format(u=username))
            return redirect(url_for('signup'))

        flash("User account has been created.")
        return redirect(url_for("login"))

    return render_template("signup.html")


@app.route("/", methods=["GET", "POST"])
@app.route("/login/", methods=["GET", "POST"])
def login():
    """
    Provides login functionality by rendering login form on get request.
    On post checks password hash from db for given input username and password.
    If hash matches redirects authorized user to home page else redirect to
    login page with error message.
    """

    if request.method == "POST":
        username = request.form['username']
        password = request.form['password']

        if not (username and password):
            flash("Username or Password cannot be empty.")
            return redirect(url_for('login'))
        else:
            username = username.strip()
            password = password.strip()

        user = User.query.filter_by(username=username).first()

        if user and check_password_hash(user.pass_hash, password):
            session[username] = True
            return redirect(url_for("user_home", username=username))
        else:
            flash("Invalid username or password.")

    return render_template("Login.html")

@app.route("/user/<username>/")
def user_home(username):
    """
    Home page for validated users.

    """
    if not session.get(username):
        abort(401)
  
    return render_template("HomePage.html", username=username)

@app.route('/predict', methods=['GET', 'POST'])
def predict():

    return render_template("Predict.html")

@app.route('/predict/move_forward', methods=['GET', 'POST'])
def move_forward():  
        jsdata = request.get_data()
        imgstr = re.search(b'data:image/jpeg;base64,(.*)', jsdata).group(1)
        image_bytes = io.BytesIO(base64.b64decode(imgstr))
        output=open('temp.jpg', 'wb')
        decoded=base64.b64decode(imgstr)
        output.write(decoded)
        output.close()
        prediction_message, score = camera.get_predictions()
        return jsonify({'PredMessage': prediction_message, 'PredScore': score * 100})


if __name__ == '__main__':
    app.run(host='localhost', debug=True)
