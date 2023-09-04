from flask import Flask,session,render_template,request,redirect,g,url_for
from pymongo import MongoClient

app=Flask(__name__)

client=MongoClient()
client=MongoClient('mongodb://localhost:27017/')

db=client['Hackathon']
app.secret_key = 'password'
users=db['users']

@app.route('/')
def index():
    if request.method=='POST':
        pname=request.form['pname']

        user = db.users.find_one(
            {'username': pname})
        
        if user:
            hist1=user.get('history1')
            hist1.append(pname)
            db.users.update_one({'username':session['user']},{'$set':{'history1':hist1}})
            no_of_box=len(hist1)
            return render_template('chat1.html',no_of_box=no_of_box,hist1=hist1)
        else:
            return "Wrong Username"

    return render_template('chat1.html')
if __name__ == '__main__':
    app.run(debug=True)