from flask import Flask,session,render_template,request,redirect,g,url_for
from pymongo import MongoClient
from youtubesearchpython import VideosSearch
from youtube_transcript_api import YouTubeTranscriptApi

app=Flask(__name__)

client=MongoClient()
client=MongoClient("mongodb://mongo:Az9PXoD6MNZrOOe6clcV@containers-us-west-144.railway.app:7025")

db=client['Hackathon']
app.secret_key = 'password'
users=db['users']

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/signup', methods=['GET','POST'])
def signup():

    if request.method=='POST':
        firstname = request.form['firstname']
        lastname = request.form['lastname']
        username = request.form['email']
        password = request.form['password']
        age = request.form['age']
        disability = request.form['disability']
        hist1=[]
        hist2=[]
        hist3=[]
        subtitle=""
        id=""

        if db.users.find_one({'username': username}):
            return render_template('signup.html', result="Username already exists")
        
        user_data = {'username': username, 'password': password,
                     'firstname': firstname, 'lastname': lastname,
                     'history1':hist1,'history2':hist2, 'history3':hist3,
                     'age':age, 'disability':disability, 'subtitle':subtitle,'id':id}
        db.users.insert_one(user_data)

        session['user'] = username
        
        return redirect(url_for('home'))
    
    return render_template('signup.html')

@app.route('/login', methods=['GET','POST'])
def login():

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        user = db.users.find_one(
            {'username': username, 'password': password})

        if user:
            session['user'] = username
            return redirect(url_for('home'))
        else:
            return 'invalid username or password'

    return render_template('login.html')

@app.route('/home', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        to_search = request.form['ytsearch']

        videosSearch = VideosSearch(to_search, limit=1)
        results = videosSearch.result()
        f_vdo = results["result"][0]
        link = f_vdo["link"]
        sep_l = link.split('=')
        id = sep_l[-1]
        transcript = YouTubeTranscriptApi.get_transcript(id)
        script = ""
        for text in transcript:
            t = text["text"]
            if t != '[Music]':
                script += t + " "

        subtitle = script
        no_of_words = len(script.split())

        if subtitle:
            user = db.users.find_one({'username': session['user']})
            if user:
                db.users.update_one({'username':session['user']},{'$set':{'subtitle':subtitle}})
                db.users.update_one({'username':session['user']},{'$set':{'id':id}})
                
            return redirect(url_for('extract'))

    return render_template('main.html')


@app.route('/extract', methods=['GET', 'POST'])
def extract():
    user = db.users.find_one({'username': session['user']})
    if user:
        subtitle=user.get('subtitle') 
        id=user.get('id') 
    return render_template('extract.html', subtitle=subtitle,id=id)

@app.route('/chat', methods=['GET','POST'])
def chat():
    if request.method=='POST':
        msg=request.form['msg']

        user = db.users.find_one(
            {'username': 'madu@gmail.com'})
        
        if user:
            hist1=user.get('history1')
            hist1.append(str(session['user']+" : "+msg))
            db.users.update_one({'username':'madu@gmail.com'},{'$set':{'history1':hist1}})
            no_of_box=len(hist1)
        return render_template('chat1.html',no_of_box=no_of_box,hist1=hist1)
    else:
        user = db.users.find_one({'username': 'madu@gmail.com'})
        if user:
            hist1=user.get('history1')
            no_of_box=len(hist1)
        return render_template('chat1.html',no_of_box=no_of_box,hist1=hist1)

# @app.route('/personal', methods=['GET','POST'])
# def personal():
#     mname=request.args["pname"]
#     user = db.users.find_one({'username': session['user']})
#     if user:
#         l=user.get(mname)
#         length=len(l)
#     if request.method=='POST':
#         chat=request.form['chat']
#         l=user.get(mname)
#         l.append(str(session['user']+":"+chat))
#         db.users.update_one({'username':session['user']},{'$set':{mname:l}})

        
        

if __name__ == '__main__':
    app.run(debug=True)