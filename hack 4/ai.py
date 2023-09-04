import wolframalpha
from flask import Flask,session,render_template,request,redirect,g,url_for
from pymongo import MongoClient

app=Flask(__name__)

client=MongoClient()
client=MongoClient('mongodb://localhost:27017/')

db=client['HackathonChatBot']
app.secret_key = 'password'
users=db['users']

client= wolframalpha.Client('6WAEP9-R9GHYET35U')

@app.route('/',methods=['GET','POST'])
def api():
    if request.method=='POST':
        query=request.form['dbt']
        res = client.query(query)
        output=next(res.results).text
        return render_template('api.html',output=output,query=query)
    return render_template('api.html')

if __name__ == '__main__':
    app.run(debug=True)


