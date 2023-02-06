from flask import Flask, redirect, render_template
import firebase_admin
from firebase_admin import db
import os
from dotenv import dotenv_values

config = dotenv_values(".env")

# gives our pythong application access to our db
cred_obj = firebase_admin.credentials.Certificate(config.SERVICE_ACCOUNT_KEY)
# have access to my database
default_app = firebase_admin.initialize_app(cred_obj, {
    'databaseURL': 'https://shrink-the-link-default-rtdb.firebaseio.com/'
})
# initialize the flask application
# creating app and setting static folder to the build that we create in our react app
app = Flask(__name__, static_folder='./build/static',
            template_folder="./build")


# home route which will redirect to /app which is client page
@app.route("/")
def hello_world():
    return redirect("/app")


# if user goes through /app we render the template which is the html page of our build react app
@app.route("/app")
def homepage():
    return render_template('index.html')


# method that goes through db and redirects to the long URL
# fetching the uniquely generated key given to user (or the alias that user inputted)
@app.route('/<path:generatedKey>', methods=['GET'])
def fetch_from_firebase(generatedKey):
    ref = db.reference("/" + generatedKey)
    data = ref.get()
    if not data:
        return '404 not found'
    else:
        longURL = data['longURL']
        return redirect(longURL)
