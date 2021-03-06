from flask import Flask, render_template, send_from_directory, request,redirect, url_for
from flask_login import current_user, login_user, logout_user, login_required, LoginManager
from flask_sqlalchemy import SQLAlchemy
from Project import app, db
from Project.models import Electives,User, Base
from flask_restful import Api
from Project.config import Config
from flask_migrate import Migrate
from flask import jsonify
import xlrd
from collections import OrderedDict
import simplejson as json


app = Flask(__name__)

api = Api(app)
app.config.from_object(Config)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
db = SQLAlchemy(app)
migrate = Migrate(app, db)
Base.metadata.drop_all(bind=db.engine)
Base.metadata.create_all(bind=db.engine)
# cors = CORS(app, resources={r"/home/*": {"origins": "*"}})

import Project.models
@app.route('/')
def index():
    return render_template('index.html')


@app.route('/Frontend/<path:path>')
def send_fe(path):
    return send_from_directory('Frontend', path)


@app.route('/home')
def home():
    return "Hello World!"


@app.route('/list')
def openlist():
    return render_template('list.html')


@app.route('/recommend')
def rec():
    return render_template('recme.html')

@app.route('/electiveDesc')
def desc():
    return render_template('description.html')


@app.route('/elective')
def getElectiveInfo():
	wb = xlrd.open_workbook('elective_datasheet.xlsx')
	sh = wb.sheet_by_index(0)
	electiveName=request.args.get('name')
	rownum=-1
	for i in range(1, sh.nrows):
		row=sh.row(i)
		if (row[1].value==electiveName):
			rownum=i
	elective = OrderedDict()
	row_values = sh.row_values(rownum)
	elective['Elective_no'] = row_values[0]
	elective['Course_name'] = row_values[1]
	elective['Description'] = row_values[2]
	elective['Teacher'] = row_values[3]
	elective['Specialization']= row_values[4]
	elective['Prerequisites'] = row_values[5]
	return json.dumps(elective)

@app.route('/electiveList')
def getElectiveList():
	wb = xlrd.open_workbook('elective_datasheet.xlsx')
	sh = wb.sheet_by_index(0)
	sem=request.args.get('sem')
	interests = request.args.get('interest')
	interests_list=['0']
	elective_list=[]
	if(len(sem)==1):
		for i in interests:
			interests_list.append(i)
		for i in range(1,sh.nrows):
			row=sh.row(i)
			if(int(sem)-3>=int(row[0].value) and (str(int(row[6].value)) in interests_list)):
				#elective_list.append(row[1].value)
				elective = OrderedDict()
				elective['Course_name']=row[1].value
				elective_list.append(elective)
		return jsonify(elective_list)
	else:
		for i in range(1,sh.nrows):
			row=sh.row(i)
			elective = OrderedDict()
			elective['Course_name']=row[1].value
			elective_list.append(elective)
		return jsonify(elective_list)




@app.route('/recommend_st2')
def recc2():
    return render_template('recme2.html')
@app.route('/login', methods=['POST','GET'])
def login():
	if(request.method=='GET'):
		return render_template('login.html')
	if(request.method=='POST'):
		email = request.form['email']
		password= request.form['password']
		headers = {"Content-Type": "application/json"}
		'''if current_user.is_authenticated:
			return jsonify({"description":"The user is already logged in","url" : url_for('index')}),200,headers
		headers = {
    		"Content-Type": "application/json",
    		}
		'''
		user = User.query.filter_by(email=email).first()
		if user is None:
			return jsonify({"description" : "1"}), 200, headers

		if password != user.password :
			return jsonify({"description" : "2"}),200,headers

		#login_user(user,remember=True)
		next_page= None
		if not next_page or url_parse(next_page).netloc != '' :
			next_page = "http://127.0.0.1/list.html" #else default next page is home
		print("a")
		return jsonify({"description" : "3", "url": "/list"}),200,headers
@app.route('/signup',methods=['POST','GET'])
def signup():
	if(request.method=='POST'):
		headers = {"Content-Type": "application/json"}
		if current_user.is_authenticated:
			return jsonify({"description" : "1" , "url" : url_for('index')}),200,headers
		username = request.form["userName"]
		email = request.form["email"]
		password = request.form["password"]
		sem= request.form["sem"]
		user = User.query.filter_by(username=username).first()
		if user is not None:
			return jsonify({"description" : "2"}),200,headers

		user = User.query.filter_by(email=email).first()
		if user is not None:
			return jsonify({"description" : "3"}),200,headers
		user = User(username = username, email= email, semester=sem, password=password)
		#user.set_password(password)
		db.session.add(user)
		db.session.commit()
		print(User.query.all())
		#return jsonify({"description" : "4","url" : "WE have to give a url"}),200,headers
		return jsonify({"description" : "4", "url": url_for('login')}),200,headers

	if(request.method=='GET'):
		return render_template('register.html')


if __name__ == '__main__':
    app.run(debug=True)
