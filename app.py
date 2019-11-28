from flask import Flask, request, render_template, redirect, url_for
import csv , pycurl , json
import settings

app = Flask(__name__)

engine = create_engine('mysql+mysqlconnector://' + MYSQL_DATABASE_USER + ':' + MYSQL_DATABASE_PASSWORD + 
	'@' + MYSQL_DATABASE_HOST + '/' + MYSQL_DATABASE_DB)

session = sessionmaker()
session.configure(bind=engine)
s = session()

@app.route('/')
def home():
    return 'Bienvenue !' + MYSQL_DATABASE_USER

@app.route('/gaz', methods=['GET','POST'])
def save_gazouille():
	if request.method == 'POST':
		print(request.form)
		dump_to_csv(request.form)
		return redirect(url_for('timeline'))
		#return "OK"
	if request.method == 'GET':
		return render_template('formulaire.html')

@app.route('/timeline/csv', methods=['GET'])
def timeline_csv():
	gaz = parse_from_csv()
	return render_template("timeline.html", gaz = gaz)

@app.route('/timeline/csv/<username>', methods=['GET'])
def timeline_csv_user(username):
	gaz = parse_from_csv_by_user(username)
	return render_template("timeline.html", gaz = gaz)


@app.route('/timeline', methods=['GET'])
def timeline():
	allTweet = getAllTweet()
	return render_template("timeline.html", allTweet = allTweet)
	

def getAllTweet():
	allTweet = []
	for p in s.query(Form).all():
    	allTweet.append(p)

    return allTweet

@app.route('/timeline/<username>', methods=['GET'])
def timeline_by_user(username):
	allTweetByUser = getTweetByUser(username)
	return render_template("timeline.html", allTweet = allTweetByUser)

def getTweetByUser(username):
	allTweetByUser = []
	for p in s.query(Form).filter_by(username=username & len(message) <= 280):
    	allTweetByUser.append(p)

    return allTweetByUser



def parse_from_csv_by_user(username):
	gaz = []
	with open('./gazouilles.csv', 'r') as f:
		reader = csv.reader(f)
		for row in reader:
			if len(row[1] <= 280 & row[0] == 'username') 
				gaz.append({"user":row[0], "text":row[1]})
	return gaz	

def parse_from_csv():
	gaz = []
	with open('./gazouilles.csv', 'r') as f:
		reader = csv.reader(f)
		for row in reader:
			if len(row[1] <= 280) 
				gaz.append({"user":row[0], "text":row[1]})
	return gaz

def dump_to_csv(d):
	donnees = [d["user-name"],d["user-text"] ]
	with open('./gazouilles.csv', 'a', newline='', encoding='utf-8') as f:
		writer = csv.writer(f)
		writer.writerow(donnees)


@app.route('/timeline/delete/<int:id>')
def timeline_delete_tweet(id):
	s.query(Tweet).filter_by(id=id).delete()
	s.commit()

	return redirect(url_for('timeline'))


@app.route('/timeline/add' , method = ['POST'])
def timeline_add_tweet():
	tweet = Tweet(title="depuis SQLAlchemy", message="message",
	            gender=False, like=2)
	s.add(form)
	s.commit()