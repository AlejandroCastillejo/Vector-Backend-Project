# from flask import Flask, request, jsonify
# from sqlalchemy import create_engine, exists
# from sqlalchemy.orm import sessionmaker
from kafka import KafkaConsumer
from json import loads
# from models import Base, Continent, Country, City
from db_manager import dbManager

# engine = create_engine('sqlite:///backend_project.db')
# Base.metadata.bind = engine
# DBSession = sessionmaker(bind=engine)
# session = DBSession()

# app = Flask(__name__) 

db = dbManager()   #crete object of dbManager class

consumer = KafkaConsumer(
    'continent',
     bootstrap_servers=['localhost:9092'],
     auto_offset_reset='earliest',
     enable_auto_commit=True,
     group_id='my-group',
     value_deserializer=lambda x: loads(x.decode('utf-8')))


def runKafkaConsumer():
    for message in consumer:
        print(message)
        if message.topic == 'continent':
            continentsFunction(message)
        elif message.topic == 'country':
            countriesFunction(message)
        else:
            pass


# @app.route("/continent", methods = ['POST', 'PUT', 'DELETE'])
def continentsFunction(_message):

    # name = request.args.get('name')
    # population = request.args.get('population', '') #if arg is not provided, default: empty string
    # area = request.args.get('area', '')
    req_method = _message.value['method']
    print 'req_method: ', req_method

    continent_args = ['name', 'population', 'area']
    for arg in continent_args:
        try:
            exec("%s = _message.value['args']['%s']"% (arg, arg))
        except KeyError:
            exec("%s = ''"% arg)
    # try:
    #     name = message.value['args']['name']
    # except KeyError:
    #     name = ''
    # try:
    #     population = message.value['args']['population']
    # except KeyError:
    #     population = ''
    # try:
    #     area = message.value['args']['area']
    # except KeyError:
    #     area = ''

    # Call this method to create a new continent
    # if request.method == 'POST':
    if req_method == 'POST':
        if name == '':
            print ("Error: 'name' param can't be empty")
            return ("Error: 'name' param can't be empty")
        elif db.continentExists(name):
            print ("Error: '%s' entry already exists on 'continents' table. Please use PUT method to update it"% name)
            return ("Error: '%s' entry already exists on 'continents' table. Please use PUT method to update it"% name)
        else:
            print (name, "added to 'continents' table")
            return db.createNewContinent(name, population, area) 
    #Call this method to update a specific continent
    # if request.method == 'PUT':
    if req_method == 'PUT':
        # if session.query(exists().where(Continent.name == name)).scalar():
        if db.continentExists(name):
            return db.updateContinent(name, population, area)
        else:
            return ("Error: '%s' entry does not exists on 'continents' table. Please use POST method to create it"% name)
    #Call this method to delelte a continent
    # elif request.method == 'DELETE':
    elif req_method == 'DELETE':
        # if session.query(exists().where(Continent.name == name)).scalar():
        if db.continentExists(name):
            return db.deleteContinent(name)
        else:
            return ("Error: '%s' entry cannot be deleted. It does not exists on 'continents' table."% name)


# @app.route("/country", methods = ['POST', 'PUT', 'DELETE'])
def countriesFunction(_message):
    # name = request.args.get('name')
    # continent = request.args.get('continent', '')
    # population = request.args.get('population', '')
    # area = request.args.get('area', '')
    # hospitals = request.args.get('hospitals', '')
    # national_parks = request.args.get('national_parks', '')
    # rivers = request.args.get('rivers', '')
    # schools = request.args.get('schools', '')
    
    req_method = _message.value['method']
    print 'req_method: ', req_method


    country_args = ['name', 'continent', 'population', 'area', 'hospitals', 
                    'national_parks', 'rivers', 'schools']
    for arg in country_args:
        print arg
        try:
            exec("%s = _message.value['args']['%s']"% (arg, arg))
        except KeyError:
            exec("%s = ''"% arg)

# Call this method to create a new country
    if req_method == 'POST':
        if name == '':
            return "Error: 'name' param can't be empty"
        elif countryExists(name):
        # elif db.
            return ("Error: '%s' entry already exists on 'countries' table. Please use PUT method to update it"% name)
        else:
            print (name, "added to 'countries' table")
            return db.createNewCountry(name, continent, population, area, hospitals, national_parks, rivers, schools) 

    #Call this method to update a specific country
    if req_method == 'PUT':
        if countryExists(name):
            return db.updateCountry(name, continent, population, area, hospitals, national_parks, rivers, schools)
        else:
            return ("Error: '%s' entry does not exists on 'countries' table. Please use POST method to create it"% name)

    #Call this method to delelte a country
    elif req_method == 'DELETE':
        if countryExists(name):
            return db.deleteCountry(name)
        else:
            return ("Error: '%s' entry cannot be deleted. It does not exists on 'countries' table."% name)






if __name__ == '__main__':
    print "Writer for broker running"
    runKafkaConsumer()

    # app.debug = True
    # app.run(host='0.0.0.0', port=5000)	