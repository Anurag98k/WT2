from flask_restful import Resource,reqparse,fields,marshal
from flask_login import current_user, login_user, logout_user, login_required
from Project.views import userbase,extra,home
from flask import url_for,request
from Project.models import User,load_user
from werkzeug.urls import url_parse
from flask_cors import CORS,cross_origin
from flask import jsonify
from flask import session
headers = {"Content-Type": "application/json"}
class Login(Resource):
	@cross_origin(origins="http://127.0.0.1:4200",supports_credentials=True,headers=['Content-Type'])
	def post(self):
		json_data = request.get_json(force=True)
		if current_user.is_authenticated:
			print("------------------")
			headers = {"Content-Type": "application/json"}
			return jsonify({"description":"The user is already logged in","url" : url_for('userbase')}),200,headers
		email = json_data["email"]
		print(email)
		password = json_data["password"]
		headers = {
    		"Content-Type": "application/json",
    		}
		if email is None :
			return jsonify({"description":"username is required"}),200,headers
		if password is None :
			return jsonify({"description":"password is required"}),200,headers

		user = User.query.filter_by(email=email).first()
		if user is None:
			print("okkk")
			return jsonify({"description" : "The username is invalid"}), 200, headers

		if not user.check_password(password) :
			return jsonify({"description" : "The password is incorrect"}),200,headers

		login_user(user,remember=True)
		next_page= None
		if not next_page or url_parse(next_page).netloc != '' :
			next_page = "http://127.0.0.1/home" #else default next page is home
		return jsonify({"decription" : "The user has been successfully logged in","url" : next_page,"userId" : current_user.id}),200,headers


#As of now CORS is not working with login_required decorator.ALternative is to use current_user.is_authenticated as Akhil suggested but this wont support next redirect.
#To do that we have to add functionality on the client side i.e. front end.
class Logout(Resource):
	@cross_origin(origins="*",supports_credentials=True)
	@login_required
	def get(self):
		logout_user()
		return jsonify({"description" : "The user has been successfully logged out","url" : url_for('extra')}),200,headers