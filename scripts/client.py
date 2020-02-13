from flask import Flask, request, jsonify
from json import dumps
from kafka import KafkaProducer

app = Flask(__name__) 

producer = KafkaProducer(bootstrap_servers=['localhost:9092'],
                         value_serializer=lambda x: 
                         dumps(x).encode('utf-8'))

@app.route("/continent", methods = ['POST', 'PUT', 'DELETE'])
def continentFunction():
    msg = {'method': request.method, 'args': request.args}
    producer.send('continent', value = msg)
    return jsonify(msg)

@app.route("/country", methods = ['POST', 'PUT', 'DELETE'])
def countryFunction():
    msg = {'method': request.method, 'args': request.args}
    producer.send('country', value = msg)
    return jsonify(msg)

if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=5000)	