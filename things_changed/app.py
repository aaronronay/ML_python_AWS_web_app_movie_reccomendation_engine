from flask import Flask,render_template,url_for,request,session,redirect,flash,jsonify
from flask_pymongo import PyMongo
import bcrypt
from scrape import theater_scrape

app=Flask(__name__)

app.config['MONGO_DBNAME'] = 'mongologinexample'
app.config['MONGO_URI'] = 'mongodb://localhost:27017/hollywoodDB'
mongo=PyMongo(app)

@app.route("/")
def index():
	
	if 'username' in session:
		return render_template('index.html',user=session['username'],logged=True)
	return render_template('index.html',logged=False)
	
	#TO BE REMOVED WHEN LOGIN DONE, TOP IS REAL CODE#
	
	# if 'username' in session:
		# return render_template('index.html',user=session['username'],logged=True)
	# return render_template('index.html',user='motherfucker',logged=True)
	
@app.route("/movies")
def movies():
	ratings_data=list(mongo.db.ratings.find()),
	movies_data=list(mongo.db.movies.find())
	return render_template("movies.html",movies_data=movies_data,ratings_data=ratings_data)

@app.route("/ratings")
def ratings():
	ratings_data=list(mongo.db.ratings.find())
	movies_data=list(mongo.db.movies.find())
	return render_template("ratings.html",movies_data=movies_data,ratings_data=ratings_data)

@app.route("/current")
def current():
	ratings_data=list(mongo.db.ratings.find())
	movies_data=list(mongo.db.movies.find())
	if session['username']:
		return render_template("current.html",user=session['username'])
	return render_template("current.html",user=None)
	

@app.route("/register", methods=['POST','GET'])
def register():
	if request.method == 'POST':
		users = mongo.db.users
		existing_user = users.find_one({'name':request.form['username']})
		
		if existing_user is None:
			hashpass = bcrypt.hashpw(request.form['pass'].encode('utf-8'), bcrypt.gensalt())
			users.insert_one({'name': request.form['username'],'password': hashpass,'zipcode':request.form['zip']})
			session['username'] = request.form['username']
			return redirect(url_for('index'))
	return render_template("register.html")

#import jsonify
#from scrape import theater_scrape
@app.route("/map")
def map():
	return render_template("map.html")

@app.route('/scrape')
def scrape():
    return jsonify(theater_scrape())
	
@app.route("/recommend")
def recommend():
	ratings_data=list(mongo.db.ratings.find())
	movies_data=list(mongo.db.movies.find())
	return render_template("index.html",movies_data=movies_data,ratings_data=ratings_data)
	
	
@app.route('/logout')
def logout():
	session.clear()
# session.pop('username', None)
	return redirect(url_for('index'))
	
	
@app.route('/login',methods=['POST'])
def login():
	users = mongo.db.users
	login_user = users.find_one({'name': request.form['username']})
	if login_user:
		if bcrypt.hashpw(request.form['pass'].encode('utf-8'), login_user['password']) == login_user['password']:
			session['username'] = request.form['username']
			return redirect(url_for('index'))
	flash('Invalid Username/Password')
	return redirect(url_for('index'))
	
# @app.route('/theater')
# def theater():

	
	
	

	
if __name__ == "__main__":
	app.secret_key='nfojern76'
	app.run(debug=True)