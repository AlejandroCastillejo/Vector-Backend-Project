from user_model import logBase, User
from flask import Flask, request, jsonify, abort, url_for, g
from json import dumps
from kafka import KafkaProducer
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy import create_engine
from flask_httpauth import HTTPBasicAuth

auth = HTTPBasicAuth() 

log_engine = create_engine('sqlite:///users.db')

logBase.metadata.bind = log_engine
DBSession = sessionmaker(bind=log_engine)
session = DBSession()

app = Flask(__name__) 

#Kafka producer
producer = KafkaProducer(bootstrap_servers=['localhost:9092'],
                         value_serializer=lambda x: 
                         dumps(x).encode('utf-8'))


#Logging functions

@auth.verify_password
def verify_password(username, password):
    print ("Looking for user %s" % username)
    user = session.query(User).filter_by(username = username).first()
    if not user: 
        print ("User not found")
        return False
    elif not user.verify_password(password):
        print ("Unable to verify password")
        return False
    else:
        g.user = user
        return True

@app.route('/new_user', methods = ['POST'])
def new_user():
    username = request.args.get('username')
    password = request.args.get('password')
    if username is None or password is None:
        print ("missing arguments")
        abort(400) 
    
    user = session.query(User).filter_by(username=username).first()
    if user is not None:
        print ("existing user")
        return jsonify({'message':'user already exists'}), 200#, {'Location': url_for('get_user', id = user.id, _external = True)}
        
    user = User(username = username)
    user.hash_password(password)
    session.add(user)
    session.commit()
    return jsonify({ 'username': user.username }), 201#, {'Location': url_for('get_user', id = user.id, _external = True)}



#app functions

@app.route("/continent", methods = ['POST', 'PUT', 'DELETE'])
@auth.login_required
def continentFunction():
    msg = {'method': request.method, 'args': request.args}
    producer.send('continent', value = msg)
    return jsonify(msg)

@app.route("/country", methods = ['POST', 'PUT', 'DELETE'])
@auth.login_required
def countryFunction():
    msg = {'method': request.method, 'args': request.args}
    producer.send('country', value = msg)
    return jsonify(msg)

if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=5000)	