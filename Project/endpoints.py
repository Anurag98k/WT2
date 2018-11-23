from Project import api
from flask_restful import Resource
from Project.signup import SignUp
from flask_login import login_required

api.add_resource(SignUp,'/signuppp',endpoint="signup")
