from flask import Flask, request

# creating Flask object
app = Flask(__name__)


# create an in-memory database
tasks= [
    {
        'id': 1,
        'title': 'Buy groceries',
        'description': 'Milk, Cheese, Pizza, Fruit, Tylenol',
        'done': False
    },
    {
        'id': 2,
        'title': 'Learn Python',
        'description': 'Need to find a good Python tutorial on the web',
        'done': False
    },
    {
        'id': 3,
        'title': 'Learn java',
        'description': 'Need to find a good java tutorial on the web',
        'done': False
    }
]


# Get all the records from the json file
@app.route("/get_data/")
def get_alldata():
    try:
        return {"statusCode": 200, 
                "message":"Data Fetched Succesfully",
                'Task':tasks}, 200
    except:
        return{"statusCode":404, "Error":"Something went wrong"}, 404

# Get a single record from the file
@app.route('/get_data/<task_id>/')
def get_data(task_id):
    task=[]
    for task in tasks:
        if task['id'] ==int(task_id):
            return {"statusCode": 200, 
                    "message":"Data Fetched Succesfully",
                    "task":task}, 200
    return {"statusCode":404,
            "message":"Value is not defined"}, 404


# Inserting the new data to the file
@app.route('/insert_data', methods=['post'])
def addData():
    if not request.json or not 'title' in request.json:
        return {"statusCode":400, "message":"You missed something"}, 400
    resp_data = request.get_json()
    print (resp_data)
    for task in tasks:
        if task ['id'] == resp_data['id']:
            return {"statusCode":400, "message":"Data is Duplicated"}, 400
    tasks.append(resp_data)
    return {"statusCode":201, "message":"Data Added Succesfully"}, 201


# modifying the data in the file
@app.route('/new/<int:task_id>', methods=['put'])
def update_task(task_id):
    task = [task for task in tasks if task['id'] == task_id]
    if not task:
        return {"statusCode":304, "message": "You enter invalid id"}, 304

    else:
        task[0]['title'] = request.json.get('title', task[0]['title'])
        task[0]['description'] = request.json.get('description', task[0]['description'])
        task[0]['done'] = request.json.get('done', task[0]['done'])
        return {"statusCode":201, "message": "successfully modified"}, 201


# modifying the data in the file
@app.route('/items/<int:item_id>', methods=['PUT'])
def update_item(item_id):
    try:
        # Get the request data
        data = request.get_json()
        if not data:
            return {"statusCode":304, "message":"Data not found"}, 304
        # Update the item with the provided data
        tasks[item_id] = data
        return {"statusCode":201, "message":"Item updated successfully"}, 201
    except:
        return {"statusCode":500, "message":"Sever is not responding"}, 500 


# Delete the record from the file
@app.route('/delete/<test>', methods=['Delete'])
def del_task(test):
    for task in tasks:
        if task['id'] == int(test):
               tasks.remove(task)
    return {"statusCode":200, "message":"Deleted the record"}, 200


# Running the code
if __name__ == "__main__":
    app.run(debug=True)
