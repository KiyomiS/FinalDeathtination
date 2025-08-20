from flask import Flask, jsonify, abort, request, url_for, redirect
from dataLayer import loadData

app = Flask(__name__)

records = loadData("2011_data.csv")

#=================start home page========================
@app.route('/', methods = ['POST', 'GET'])
def home():
    if request.method == 'POST':
        return redirect(url_for('get_records'))
    else:
        return redirect(url_for('get_records'))
#=================== end home page ======================

#=================== start records page =================

@app.route('/records')
def get_records():
    return jsonify({'records': records})

#=================== end records page ===================


#================= start Get methods ====================

@app.route('/records/sex/<string:record_sex>', methods=['GET'])
def get_recordBySex(record_sex):
    record = [record for record in records if record['Sex'] == record_sex] #search until match found
    if len(record) == 0:
        abort(404) #no record found with matching index, abort
    return jsonify({'record': record[0]}) #return first match

@app.route('/records/age/<int:record_age>', methods=['GET'])
def get_recordByAge(record_age):
    record = [record for record in records if record['Age'] == record_age]
    if len(record) == 0:
        abort(404) 
    return jsonify({'record': record[0]})

@app.route('/records/month/<string:record_month>', methods=['GET'])
def get_recordByMonth(record_month):
    record = [record for record in records if record['Month'] == record_month]
    if len(record) == 0:
        abort(404) 
    return jsonify({'record': record[0]})

#================== End Get Methods ===================

#================== Start Post Methods ================

@app.route('/records', methods=['POST'])
def create_record():
        if not request.json: #must be in json format
            abort(400)
        record = {
            'Sex': request.json['Sex'],
            'Age': request.json['Age'],
            'Race': request.json['Race'],
            'Month': request.json['Month'],
            'MoD': request.json['MoD'],
        }
        records.append(record) #add task to existing databse
        return jsonify({'record': record})

#================== End Post Methods ==================

if __name__ == '__main__':
    app.run(debug=True)
