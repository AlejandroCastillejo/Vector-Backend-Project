from flask import Flask, request, jsonify
from sqlalchemy import create_engine, exists
from sqlalchemy.orm import sessionmaker

from models import Base, Continent, Country, City
import time

engine = create_engine('sqlite:///backend_project.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()

app = Flask(__name__) 

# @app.route("/")
@app.route("/continent", methods = ['POST', 'PUT', 'DELETE'])
def continentsFunction():
    name = request.args.get('name')
    population = request.args.get('population', '') #if arg is not provided, default: empty string
    area = request.args.get('area', '')
    
    # Call this method to create a new continent
    if request.method == 'POST':
        if name == '':
            return "Error: 'name' param can't be empty"
        elif session.query(exists().where(Continent.name == name)).scalar():
            return ("Error: '%s' entry already exists on 'continents' table. Please use PUT method to update it"% name)
        else:
            print (name, "added to 'continents' table")
            return createNewContinent(name, population, area) 

    #Call this method to update a specific continent
    if request.method == 'PUT':
        if session.query(exists().where(Continent.name == name)).scalar():
            return updateContinent(name, population, area)
        else:
            return ("Error: '%s' entry does not exists on 'continents' table. Please use POST method to create it"% name)

    #Call this method to delelte a continent
    elif request.method == 'DELETE':
        if session.query(exists().where(Continent.name == name)).scalar():
            return deleteContinent(name)
        else:
            return ("Error: '%s' entry cannot be deleted. It does not exists on 'continents' table."% name)


@app.route("/country", methods = ['POST', 'PUT', 'DELETE'])
def countriesFunction():
    name = request.args.get('name')
    continent = request.args.get('continent', '')
    population = request.args.get('population', '')
    area = request.args.get('area', '')
    hospitals = request.args.get('hospitals', '')
    national_parks = request.args.get('national_parks', '')
    rivers = request.args.get('rivers', '')
    schools = request.args.get('schools', '')

# Call this method to create a new country
    if request.method == 'POST':
        if name == '':
            return "Error: 'name' param can't be empty"
        elif session.query(exists().where(Country.name == name)).scalar():
            return ("Error: '%s' entry already exists on 'countries' table. Please use PUT method to update it"% name)
        else:
            print (name, "added to 'countries' table")
            return createNewCountry(name, continent, population, area, hospitals, national_parks, rivers, schools) 

    #Call this method to update a specific country
    if request.method == 'PUT':
        if session.query(exists().where(Country.name == name)).scalar():
            return updateCountry(name, continent, population, area, hospitals, national_parks, rivers, schools)
        else:
            return ("Error: '%s' entry does not exists on 'countries' table. Please use POST method to create it"% name)

    #Call this method to delelte a country
    elif request.method == 'DELETE':
        if session.query(exists().where(Country.name == name)).scalar():
            return deleteCountry(name)
        else:
            return ("Error: '%s' entry cannot be deleted. It does not exists on 'countries' table."% name)



def createNewContinent(_name, _population, _area):
    new_continent = Continent(name = _name, population = _population, area = _area)
    session.add(new_continent)
    session.commit()
    return jsonify(Continent = new_continent.serialize)

def updateContinent(_name, _population, _area):
    continent = session.query(Continent).filter_by(name = _name).one()
    #only update entries if params are received, this way it doesn't erase previous data
    if _population != '':
        continent.population = _population
    if _area != '':
        continent.area = _area
    session.add(continent)
    session.commit()
    return jsonify(Continent = continent.serialize)
    
def deleteContinent(_name):
    continent = session.query(Continent).filter_by(name = _name).one()
    session.delete(continent)
    session.commit()
    return ("Continent '%s' deleted"% _name)

#TODO include logic validation. E.g., sum of population in countries of the same continent can't be greater than continent population

def createNewCountry(_name, _continent, _population, _area, _hospitals, _national_parks, _rivers, _schools):
    new_country = Country(name = _name, continent = _continent, population = _population, area = _area, hospitals = _hospitals, \
                            national_parks = _national_parks, rivers = _rivers, schools = _schools)
    session.add(new_country)
    session.commit()
    return jsonify(Country = new_country.serialize)

def updateCountry(_name, _continent, _population, _area, _hospitals, _national_parks, _rivers, _schools):
    country = session.query(Country).filter_by(name = _name).one()
    #only update entries if params are received, this way it doesn't erase previous data
    if _continent != '':
        country.continent = _continent
    if _population != '':
        country.population = _population
    if _area != '':
        country.area = _area
#TODO the same with the rest of params
#TODO better create a list of params and use for loop
    session.add(country)
    session.commit()
    return jsonify(Country = country.serialize)
    
def deleteCountry(_name):
    country = session.query(Country).filter_by(name = _name).one()
    session.delete(country)
    session.commit()
    return ("Country '%s' deleted"% _name)


if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=5000)	