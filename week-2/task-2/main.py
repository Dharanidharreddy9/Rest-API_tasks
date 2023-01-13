from flask import Flask
from flask_httpauth import HTTPBasicAuth


app = Flask(__name__)
auth = HTTPBasicAuth()

# Giving local data for testing
users = {
    "john": "password123",
    "sarah": "mysecretpass"
}


# Verifying the password
@auth.verify_password
def verify_password(username, password):
    if username in users:
        return users[username] == password
    return False


# login Route
@app.route("/login")
@auth.login_required
def login():
    return {"statusCode":201 ,"message":"You are authenticated!"}, 201


# This will print the users who are logedin
@app.route("/data")
@auth.login_required
def data():
    return {"statusCode":200 ,"message":"You are authenticated!", 
            "users": users}, 200


if __name__ == "__main__":
    app.run()
