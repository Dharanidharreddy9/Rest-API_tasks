from flask import Flask,request,jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_restplus import Resource, Api, fields


# Creating 
app = Flask(__name__)

# conncting the database
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=True
db = SQLAlchemy(app)
ma = Marshmallow(app)
api = Api()
api.init_app(app)


#creating a Table
class User(db.Model):
    id = db.Column(db.Integer,primary_key=True,autoincrement=True)
    name = db.Column(db.String)
    email = db.Column(db.String)
    password = db.Column(db.String)


class UserSchema(ma.Schema):
    class Meta:
        fields = ('id','name','email','password')


model = api.model('demo',{
    'name':fields.String('Enter Name'),
    'email':fields.String('Enter Email'),
    'password':fields.String('Enter Password')
})

user_schema = UserSchema()
users_schema = UserSchema(many=True)


# It has fetching all the data
@api.route('/get')
class getdata(Resource):
    def get(self):
        try:
            user = User.query.all()
            get_alldata = UserSchema(many=True).dump(user)
            return get_alldata
            # return users_schema.dump(User.query.all()), 200
        except Exception as e:
            print(e)
            return {'message' : 'Data is not fetching !!'}, 401


# It will inserting the data into the database
@api.route('/post')
class postdata(Resource):
    @api.expect(model)
    def post(self):
        try:
            user = User(name=request.json['name'],
                        email=request.json['email'],
                        password=request.json['password'])
            db.session.add(user)
            db.session.commit()
            return {'message':'Data added successfully'}, 201
        except Exception as e:
            print(e)
            return {'message' : 'Data is not Added !!'}, 304


# This will modify the data ased on ID
@api.route('/put/<int:id>')
class putdata(Resource):
    @api.expect(model)
    def put(self,id):
        try:
            user = User.query.get(id)
            user.name = request.json['name']
            user.email = request.json['email']
            user.password = request.json['password']
            db.session.commit()
            return {'message':'Data updated'}, 201

        except Exception as e:
            print(e)
            return {'message' : 'Data is not Modified !!'}, 304


# This api will delete the records based on id's
@api.route('/delete/<int:id>')
class deletedata(Resource):
    # @api.expect(model)
    def delete(self,id):
        try:
            user = User.query.get(id)
            db.session.delete(user)
            db.session.commit()
            return jsonify({'message':'Data deleted successfully'}), 200
        except Exception as e:
            print(e)
            return {'message' : 'Data is not Deleted !!'}, 304


if __name__ == '__main__':
    # with app.app_context():
    #     db.create_all()
    app.run(debug=True)
