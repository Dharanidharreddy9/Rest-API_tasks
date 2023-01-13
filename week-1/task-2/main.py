from flask import Flask, request, make_response
from flask_sqlalchemy import SQLAlchemy
import uuid # for public id
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
from datetime import datetime, timedelta
from flask_marshmallow import Marshmallow
from functools import wraps


# creates Flask object
app = Flask(__name__)
app.config['SECRET_KEY'] = 'abcd'

# database connection
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://admin:root@localhost:5432/task_2'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True


# creates SQLALCHEMY object
db = SQLAlchemy(app)
ma = Marshmallow(app)


# Database ORMs
class User(db.Model):
		id = db.Column(db.Integer, primary_key = True)
		public_id = db.Column(db.String(50), unique = True)
		name = db.Column(db.String(100))
		email = db.Column(db.String(70), unique = True)
		password = db.Column(db.String(80))


# decorator for verifying the JWT
def token_required(f):
		@wraps(f)
		def decorated(*args, **kwargs):
			token = None
			if 'x-access-token' in request.headers:
				token = request.headers['x-access-token']
			if not token:
				return {"statusCode": 401, 'message' : 'Token is missing !!'}, 401
			try:
				data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
				current_user = User.query.filter_by(public_id = data['public_id']).first()
			except Exception:
				return {"statusCode": 401, 'message' : 'Token is invalid !!'}, 401
			return f(current_user, *args, **kwargs)
		return decorated


# User Database Route this route sends back list of users(token function is run before this)
@app.route('/getuser', methods =['GET'])
@token_required
def get_all_users(current_user):
		users = User.query.all()
		output = []
		for user in users:
			output.append({
				'public_id': user.public_id,
				'name' : user.name,
				'email' : user.email
			})
		return {"statusCode": 200, 
				"message":"Data Fetching Successfully",
				"users" :output}, 200


# route for logging user in
@app.route('/login', methods =['POST'])
def login():
		auth = request.form
		if not auth or not auth.get('email') or not auth.get('password'):
			return make_response('Could not verify ', 401, {'WWW-Authenticate' : 'Basic realm ="Login required !!"'})

		user = User.query.filter_by(email = auth.get('email')).first()
		if not user:
			return make_response('Could not verify ', 401, {'WWW-Authenticate' : 'Basic realm ="User does not exist !!"'})

		if check_password_hash(user.password, auth.get('password')):
			token = jwt.encode({
				'public_id': user.public_id,
				'exp' : datetime.utcnow() + timedelta(minutes = 30)
			}, app.config['SECRET_KEY'])

			return {"statusCode": 201, "message":"Token is generated Successfully", "token":token}, 201
		return make_response('Could not verify ', 403, {'WWW-Authenticate' : 'Basic realm ="Wrong Password !!"'})


# user will signup here using the post method
@app.route('/signup', methods =['POST'])
def signup():
		data = request.form
		name, email = data.get('name'), data.get('email')
		password = data.get('password')
		user = User.query.filter_by(email = email).first()
		if not user:
			user = User(
				public_id = str(uuid.uuid1()),
				name = name,
				email = email,
				password = generate_password_hash(password)
			)
			db.session.add(user)
			db.session.commit()
			return {"statusCode":201, "message":"Successfully Registered"}, 201
		else:
			return {"statusCode":201, "message":"User already exists, Please Login"}, 202


if __name__ == "__main__":
	app.run(debug = True)
