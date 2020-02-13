from sqlalchemy import create_engine, exists
from sqlalchemy.orm import sessionmaker
from models import Base, Continent, Country, City


class dbManager:
    
    engine = create_engine('sqlite:///backend_project.db')
    Base.metadata.bind = engine
    DBSession = sessionmaker(bind=engine)
    session = DBSession()

    def createNewContinent(self, _name, _population, _area):
        new_continent = Continent(name = _name, population = _population, area = _area)
        self.validateContinentData(_name, _population, _area)
        self.session.add(new_continent)
        self.session.commit()
        # return jsonify(Continent = new_continent.serialize)

    def updateContinent(self, _name, _population, _area):
        print 'update continent'
        continent = self.session.query(Continent).filter_by(name = _name).one()
        #only update entries if params are received, this way it doesn't erase previous data
        if _population != '':
            continent.population = _population
        if _area != '':
            continent.area = _area
        self.validateContinentData(_name, _population, _area)
        self.session.add(continent)
        self.session.commit()
        # return jsonify(Continent = continent.serialize)

    def deleteContinent(self, _name):
        continent = self.session.query(Continent).filter_by(name = _name).one()
        self.session.delete(continent)
        self.session.commit()
        return ("Continent '%s' deleted"% _name)

    def continentExists(self, _name):
        # print 'debug: continent exists function'
        if self.session.query(exists().where(Continent.name == _name)).scalar():
            return True
    
#TODO include logic validation. E.g., sum of population in countries of the same continent can't be greater than continent population
    def validateContinentData(self, _name, _population, _area):
        print ('debug: validate continent data')
        try:
            countries = self.session.query(Country).filter(continent)
            print countries
        except:
            print ('no country of this continent found')




    def createNewCountry(_name, _continent, _population, _area, _hospitals, _national_parks, _rivers, _schools):
        new_country = Country(name = _name, continent = _continent, population = _population, area = _area, hospitals = _hospitals, \
                                national_parks = _national_parks, rivers = _rivers, schools = _schools)
        self.session.add(new_country)
        self.session.commit()
        # return jsonify(Country = new_country.serialize)

    def updateCountry(_name, _continent, _population, _area, _hospitals, _national_parks, _rivers, _schools):
        country = self.session.query(Country).filter_by(name = _name).one()
        #only update entries if params are received, this way it doesn't erase previous data
        if _continent != '':
            country.continent = _continent
        if _population != '':
            country.population = _population
        if _area != '':
            country.area = _area
    #TODO the same with the rest of params
    #TODO better create a list of params and use for loop
        self.session.add(country)
        self.session.commit()
        # return jsonify(Country = country.serialize)

    def deleteCountry(_name):
        country = self.session.query(Country).filter_by(name = _name).one()
        self.session.delete(country)
        self.session.commit()
        return ("Country '%s' deleted"% _name)

    def countryExists(self, _name):
        # print 'debug: country exists function'
        if self.session.query(exists().where(Country.name == _name)).scalar():
            return True
    
    