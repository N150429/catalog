from flask import Flask,redirect,url_for,render_template,request,flash
from flask_mail import Mail,Message
from random import randint 
from project_database import Register,Base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
#engine=create_engine('sqlite:///iii.db')
engine=create_engine('sqlite:///iii.db',connect_args={'check_same_thread':False},echo=True)
Base.metadata.bind=engine
DBsession=sessionmaker(bind=engine)
session=DBsession()

app=Flask(__name__)

app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT']=465
app.config['MAIL_USERNAME']='kondalaraju429@gmail.com'
app.config['MAIL_PASSWORD']='kondalarajumail.com'
app.config['MAIL_USE_TSL']=False
app.config['MAIL_USE_SSL']=True
app.secret_key = 'abc'

mail = Mail(app)
otp=randint(00000,99999)
"""@app.route("/sample")
def demo():
	return "Hello World good"

@app.route("/demo_msg")
def d():
	return "<h1>Hello demo</h1>"

@app.route("/info/details")
def demos():
	return "<h1>Hello Details</h1>"

@app.route("/details/<name>/<int:age>/<float:sal>")
def info(name,age,sal):
	return "hello {} age: {} salary: {}".format(name,age,sal)"""

@app.route("/admin")
def admin():
	return "hello admin"

@app.route("/student")
def student():
	return "hello stuednt"

@app.route("/staff")
def staff():
	return "hello staff"

@app.route("/info/<name>")
def admin_info(name):
	if name=='admin':
		return redirect(url_for('admin'))
	elif name=='student':
		return redirect(url_for('student'))
	elif name=='staff':
		return redirect(url_for('staff'))
	else:
		return "NO URL"

@app.route("/data/<name>/<int:age>/<float:salary>")
def demo_html(name,age,salary):
	return render_template('sample.html',n=name,a=age,s=salary)

@app.route("/info-data")
def info_data():
	sno="1"
	name="raju"
	department="cse"
	branch="cse1"

	return render_template('sample1.html',s_no=sno,n=name,d=department,b=branch)


data=[
{'sno':1,'n':"raju",'d':"department",'b':"cse"},
{'sno':2,'n':"nkr",'d':"french",'b':"It"},
{'sno':3,'n':"rju",'d':"department",'b':"cse"}
]
@app.route("/dummy_data")
def dummy():
	return render_template('data.html',dummy_data=data)


@app.route("/table/<int:num>")
def table(num):
	return render_template("table.html",n=num)




@app.route("/file_upload",methods=['GET', 'POST'])
def file_upload():
	return render_template("file_upload.html")


@app.route("/success",methods=['GET', 'POST'])
def success():
	if request.method=="POST":
		f=request.files['file']
		f.save(f.filename)

		return render_template("success.html",f_name=f.filename)
 
@app.route("/email",methods=['GET','POST'])
def email():
	return render_template("email.html")
@app.route("/email_verify", methods=['GET','POST'])
def verify_email():
	email = request.form['email']
	msg=Message("One Time Password", sender="kondalaraju429@gmail.com",recipients=[email])
	msg.body=str(otp)
	mail.send(msg)
	return render_template("v_email.html")

@app.route("/email_success", methods=['POST','GET'])
def email_success():
	user_otp=request.form['otp']
	if(otp==int(user_otp)):
		return  "succcess"
	return "invalid"
@app.route("/show")
def showdb():
	register=session.query(Register).all()
	return render_template("show.html",reg=register)
@app.route("/New",methods=['POST','GET'])

def addData():
	if request.method=='POST':
		newData=Register(name=request.form['name'],surname=request.form['surname'],mobile=request.form['mobile'],branch=request.form['branch'],role=request.form['role'])
		session.add(newData)
		session.commit()
		flash("Data added....")
		return redirect(url_for('showdb'))
	else:
		return render_template("new.html")


@app.route("/edit/<int:register_id>",methods=['POST','GET'])
def editData(register_id):
	editedData = session.query(Register).filter_by(id=register_id).one()
	if request.method=='POST':
		editedData.name = request.form['name']
		editedData.surname = request.form['surname']
		editedData.mobile = request.form['mobile']
		editedData.email = request.form['email']
		editedData.branch = request.form['branch']
		editedData.role = request.form['role']

		session.add(editedData)
		session.commit()
		flash("Edited successfully")
		return redirect(url_for('showdb'))
	else:
		return render_template('edit.html',register=editedData)

@app.route("/delete/<int:register_id>", methods=['POST','GET'])
def deleteData(register_id):
	deletedData =session.query(Register).filter_by(id=register_id).one()
	if request.method=='POST':	
		session.delete(deletedData)
		session.commit()
		flash("Deleted successfully")
		return redirect(url_for('showdb'))
	else:
		return render_template('delete.html',register=deletedData)

















@app.route("/")
def home():
	return render_template("home.html")



if __name__=='__main__':
	app.run(debug=True)
