import email
from flask import Blueprint, render_template,request,session,flash,redirect,url_for
from flask.json import jsonify

second=Blueprint('second',__name__,static_folder='static',template_folder='templates')
from pymongo.mongo_client import MongoClient

uri = "mongodb+srv://root:21951A67B9@cluster0.twkxqsh.mongodb.net/?retryWrites=true&w=majority"

# Create a new client and connect to the server
client = MongoClient(uri)

# Send a ping to confirm a successful connection
try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)
    

db=client['med-record']
admin=db['admin']
userRecords=db['records']


@second.route('/login')
def loginDoc():
    return render_template('adminLogin.html')

@second.route('/auth',methods=['POST','GET'])
def auth():
    if request.method=='POST':
        docMail=request.form['docMail']
        psw=request.form['psw'] 
        if admin.find_one({'_id':docMail,'psw':psw}):
            session['docMail']=docMail
            flash('You have logged in succesfully','info')
            return redirect(url_for('second.home'))
        else:
            flash('Login credentials are wrong!!!','info')
            return redirect(url_for('second.loginDoc'))
    return redirect(url_for('login'))
 
    
@second.route('/home')
def home():
    email=session['docMail']
    doctor=admin.find_one({'_id':email})
    data=userRecords.find()
    return render_template('adminHomePage.html',doctor=doctor,data=data)

@second.route('/userInfo',methods=['POST','GET'])
def userInfo():
    if request.method=='POST':
        email=request.form.get('email')
        data=userRecords.find_one({'_id':email})
        return render_template('adminUserInfo.html',data=data)
    flash('Incorrect Response!! {}'.format(email),'warning')
    return redirect(url_for('second.home'))

