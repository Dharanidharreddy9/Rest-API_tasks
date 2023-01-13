from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy

# creates Flask object
app = Flask(__name__)

# Connecting the Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://admin:root@localhost:5432/task_5'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


# first table TelemetryData which contain id,devicename,application_name,payload
class TelemetryData(db.Model):
    __tablename__ = 'telemetry_data'
    id = db.Column(db.Integer, primary_key =True)
    deviceName =db.Column(db.String, nullable = False)
    application_name =db.Column(db.String,nullable=False)
    payload = db.Column(db.JSON, default={})

    def __repr__(self):
        return self.deviceName


# second table AnalyticalData which contain id,devicename,payload1,,payload2,payload3
class AnalyticalData(db.Model):
    __tablename__ = 'analytical_data'
    id = db.Column(db.Integer, primary_key =True)
    deviceName =db.Column(db.String, nullable = False)
    payload1 = db.Column(db.Integer, default={})
    payload2 = db.Column(db.Integer, default={})
    payload3 = db.Column(db.Integer, default={})

    def __repr__(self):
        return str(self.deviceName)


# This api will inserted the dta into the Database
@app.route('/data/post_data/', methods=['POST'])
def data_create():
    data = request.get_json()
    payloads = data['payload']
    telemetry = TelemetryData(deviceName = data['deviceName'],
                              application_name=data['application_name'], 
                              payload = payloads)

    analytical = AnalyticalData(deviceName = data['deviceName'],
                                payload1 = int(payloads['payload1']),
                                payload2 = int(payloads['payload2']),
                                payload3 = int(payloads['payload3']))
    db.session.add(telemetry)
    db.session.add(analytical)
    db.session.commit()
    return {'status':'Successfull'}, 201


# DELETE the data in the TelemetryData table
@app.route('/delTelemetryData/<string:id>', methods=['DELETE'])
def deldata(id):
        delData = TelemetryData.query.get(id)
        db.session.delet(delData)
        db.session.commit()
        return {'status':'Id '+id+' is deleted in TelemetryData table'}, 200


# DELETE the data in the AnalyticalData table
@app.route('/delanalytical_data/<string:id>', methods=['DELETE'])
def delanalytical_data(id):
        delData = AnalyticalData.query.get(id)
        db.session.delete(delData)
        db.session.commit()
        return {'status':'Id '+id+' is deleted in TelemetryData table'}, 200


if __name__ == '__main__':
    # with app.app_context():
    #     db.create_all()
    app.run(debug=True)
