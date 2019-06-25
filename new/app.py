from flask import Flask,render_template,url_for,request,session,redirect,flash
from flask_pymongo import PyMongo
import bcrypt

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

@app.route("/ratings",methods=['POST','GET'])
def ratings():
	me = mongo.db.users.find_one({'name':session['username']})
	myratings=mongo.db.merge.find({'userId':me['userId']})
	return render_template("ratings.html",user=session['username'],myratings=myratings)

@app.route("/search",methods=['POST'])
def search():
	movie=mongo.db.movies.find_one({'title':request.form['title']})
	if movie:
		return render_template("ratings.html",movie_title=movie['title'],movie_number=movie['movieId'],found=True, user=session['username'])
	return render_template("ratings.html",not_found=True, user=session['username'])
		
@app.route("/rate",methods=['POST'])
def rate():
	new_rating=request.form['movieRating']
	
	person = mongo.db.users.find_one({'name':session['username']})
	mongo.db.merge.insert_one({'userId':person['userId'],'movieId':request.form['movieNumber'],'title':request.form['movieTitle'],'rating':request.form['movieRating']})
	
	return redirect(url_for('ratings'))



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
			user_num=700
			taken=True
			while taken:
				test = mongo.db.merge.find_one({'userId':user_num})
				if test is None:
					taken=False
				else:
					user_num = user_num + 1
			
			hashpass = bcrypt.hashpw(request.form['pass'].encode('utf-8'), bcrypt.gensalt())
			users.insert_one({'name': request.form['username'],'password': hashpass,'zipcode':request.form['zip'],'userId':user_num})
			session['username'] = request.form['username']
			return redirect(url_for('index'))
	return render_template("register.html")
	
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