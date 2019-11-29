from flask import Flask, request, render_template, redirect, url_for
import csv , pycurl , json
from flask_sqlalchemy import SQLAlchemy
import config
import re

app = Flask(__name__)
app.config["DEBUG"] = True

"""
Instanciation de la base de donnée
"""
db = SQLAlchemy(app)

"""
Création d'une classe Tweet selon la syntaxe objet SQLAlchemy
"""
class Tweet(db.Model):
    """
    Model Tweet
    """
    __tablename__ = 'Tweet'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64))
    message = db.Column(db.String(300))

    # methode magique pour print()
    def __str__(self):
        return "{} | {}".format(self.username, self.message)

SQLALCHEMY_DATABASE_URI = "mysql+mysqlconnector://{username}:{password}@{hostname}/{databasename}".format(
    username='arnaudadon',
    password='&Password',
    hostname='arnaudadon.mysql.eu.pythonanywhere-services.com',
    databasename='arnaudadon$gazouille',
)

app.config["SQLALCHEMY_DATABASE_URI"] = SQLALCHEMY_DATABASE_URI
app.config["SQLALCHEMY_POOL_RECYCLE"] = 299
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db.create_all()

def addMessage(d):
    content = Tweet(
        username=d["user-name"],
        message=d["user-text"]
    )
    db.session.add(content)
    db.session.commit()

@app.after_request
def add_header(response):
    """
    Definition du header
    """
    response.cache_control.max_age = 300
    response.headers['Access-Control-Allow-Origin'] = ['195.154.176.62','80.15.154.187']
    return response



@app.route('/')
def home():
    """
    Page initiale de l'application
    """
    #return 'Bienvenue sur !'
    return render_template('index.html')

@app.route('/gaz', methods=['GET','POST'])
def save_gazouille():
    """
    Fonction permettant d'afficher le formulaire ou d'enregitrer un tweet
    """
    if request.method == 'POST':
        print(request.form)
        addMessage(request.form)
        return redirect(url_for('timeline'))
        #return "OK"
    if request.method == 'GET':
        return render_template('formulaire.html')

@app.route('/timeline/csv', methods=['GET'])
def timeline_csv():
    """
    Lister les différents tweet
    """
    gaz = parse_from_csv()
    return render_template("timeline.html", gaz = gaz)

@app.route('/timeline/csv/<username>', methods=['GET'])
def timeline_csv_user(username):
    """
    Afficher la liste des tweet de l'auteur sélectionné
    """
    gaz = parse_from_csv_by_user(username)
    return render_template("timeline.html", gaz = gaz)

def parse_from_csv_by_user(username):
    """
    Parse le fichier gazouilles et affiche les différents tweet d'un utilisateur
    """
    gaz = []
    with open('./gazouilles.csv', 'r') as f:
        reader = csv.reader(f)
        for row in reader:
            if len(row[1]) <= 280 and row[0] == username:
                gaz.append({"user":row[0], "text":row[1]})
    return gaz

def parse_from_csv():
    """
    Parse le fichier gazouilles et affiche les différents tweet
    """
    gaz = []
    with open('./gazouilles.csv', 'r') as f:
        reader = csv.reader(f)
        for row in reader:
            if len(row[1]) <= 280:
                gaz.append({"user":row[0], "text":row[1]})
    return gaz

def dump_to_csv(d):
    """
    Insert les données du formulaire dans le fichier gazouilles.csv
    """
    donnees = [d["user-name"],d["user-text"] ]
    with open('./gazouilles.csv', 'a', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(donnees)

@app.route('/timeline', methods=['GET'])
def timeline():
    """
    Affiche tous les tweets de la base de donnée
    """
    allTweet = getAllTweet()
    return render_template("timeline.html", allTweet = allTweet)

def getAllTweet():
    """
    Recherche tous les tweet en base de donnée
    """
    tweetFiltered = []
    allTweet = Tweet.query.all()
    for tweet in allTweet:
        if(len(tweet.message) <= 280 and len(tweet.message) > 0):
            tweetFiltered.append(tweet)
    return tweetFiltered


@app.route('/timeline/<username>', methods=['GET'])
def timeline_by_user(username):
    """
    Fonction qui affiche tous les tweet d'un utilisateur choisie
    """
    allTweetByUser = getTweetByUser(username)
    return render_template("timeline.html", allTweet = allTweetByUser)

def getTweetByUser(username):
    """
    Fonction qui recherche en base de donnée les tweet d'un utilisateur choisie
    """
    tweetFiltered = []
    allTweetByUser = Tweet.query.filter(Tweet.username==username)
    for tweetByUser in allTweetByUser:
        if(len(tweetByUser.message) <= 280 and len(tweetByUser.message) > 0):
            tweetFiltered.append(tweetByUser)
    return tweetFiltered
