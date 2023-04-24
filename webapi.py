import flask
from flask import request, jsonify, render_template


web = flask.Flask(__name__)
web.config["DEBUG"] = True

#Determines get method
@web.route('/', methods = ['GET'])
def home():
   return "<h1>Greetings</h1><p>Welcome to car traversal detection</p><p></p>"

@web.route("/login")
def login():
   return render_template('login.html')

@web.route('/ui')
def index():
    # Getting the Video Stream on the website
    return render_template('index.html')

@web.errorhandler(404)
def page_not_found(e):
   return "<h1>404 Error</h1><p>Aw man :( No resources??.</p>", 404

web.run(host="0.0.0.0")
