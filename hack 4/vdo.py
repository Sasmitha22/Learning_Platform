from flask import Flask,session,render_template,request,redirect,g,url_for

app=Flask(__name__)

@app.route('/')
def vdoin():
    return render_template('vdoin.html')

@app.route('/vdocall')
def vdocall():
    return render_template('vdocall.html')

@app.route('/base',methods=['GET', 'POST'])
def base():
    if request.method=='POST':
        roomID = request.form['roomID']
        return redirect("/vdocall?roomID="+roomID)
    return render_template('base.html')

if __name__ == '__main__':
    app.run(debug=True)