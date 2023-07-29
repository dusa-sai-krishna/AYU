from flask import Flask,request,render_template,redirect,url_for,session,flash
from admin.second import second

app=Flask('__name__')
app.register_blueprint(second,url_prefix="/admin")
app.secret_key='key'
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
userRecords=db['records']

@app.route('/',methods=['POST','GET'])
def registration():
    return render_template('registrationPage.html')

@app.route('/submit',methods=['POST','GET'])
def user():
    if request.method=='POST':
        fullName=request.form['name']
        age=request.form['age']
        phno=request.form['phno']
        email=request.form['email']
        psw=request.form['psw']
        height=request.form['height']
        weight=request.form['weight']
        bloodGroup=request.form['bloodGroup']
        diseases = request.form.getlist('diseases')
        otherDiseases=request.form['otherDiseases']
        if otherDiseases:
            diseases.append(otherDiseases)
        additionalInfo=request.form['additionalInfo']
        data={'_id':email,'name':fullName,'age':age,'phno':phno,'psw':psw,'height':height,'weight':weight,
              'bloodGroup':bloodGroup,'diseases':diseases,'additionalInfo':additionalInfo}
        
        if userRecords.find_one({'_id':email}):
            flash('Email already exsists!!!')
            return render_template('registrationPage.html')
        else:
            userRecords.insert_one(data)
            return redirect(url_for('login'))
    else:
        return redirect('registration')
    
@app.route('/login',methods=['POST','GET'])
def login():
    return render_template('loginPage.html')


@app.route('/auth',methods=['POST','GET'])
def auth():
    if request.method=='POST':
        email=request.form['email']
        psw=request.form['psw']
        if userRecords.find_one({'_id':email,'psw':psw}):
            session['email']=email
            flash('You have logged in succesfully','info')
            return redirect(url_for('home'))
        else:
            return redirect(url_for('login'))   
        
        
@app.route('/home',methods=['POST','GET'])
def home():
    email=session['email']
    data=userRecords.find_one({'_id':email})
    return render_template('homePage.html',data=data)


@app.route('/logout')
def logout():
    if 'email' in session:
        flash('You have been logged out sucessfully','info')
    session.pop('email',None)
    return redirect(url_for('login'))

if __name__=='__main__':
    app.run(host='0.0.0.0',debug=True)      