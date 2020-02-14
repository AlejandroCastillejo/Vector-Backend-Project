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
        print ("Continent '%s' added to db"% _name)

    def updateContinent(self, _name, _population, _area):
        continent = self.session.query(Continent).filter_by(name = _name).one()
        #only update entries if params are received, this way it doesn't erase previous data
        if _population != '':
            continent.population = _population
        if _area != '':
            continent.area = _area
        self.validateContinentData(_name, _population, _area)
        self.session.add(continent)
        self.session.commit()
        print ("Continent '%s' updated"% _name)


    def deleteContinent(self, _name):
        continent = self.session.query(Continent).filter_by(name = _name).one()
        self.session.delete(continent)
        self.session.commit()
        print ("Continent '%s' deleted"% _name)

    def continentExists(self, _name):
        if self.session.query(exists().where(Continent.name == _name)).scalar():
            return True
    
    # include logic validation. E.g., sum of population in countries of the same continent can't be greater than continent population
    def validateContinentData(self, _name, _population, _area):
        countries = self.session.query(Country).filter_by(continent=_name).all()
        sum_area = 0
        sum_population = 0
        for country in countries:
            sum_area += country.area
            sum_population += country.population
        if countries != []: 
            if int(_area) < sum_area:
                print("Validation error: area of this continent must be greater than sum of it's countries area")
            else:
                print("Validation ok: area of this continent is equal or greater than sum of it's countries area")
            if int(_population) < sum_population:
                print("Validation error: population of this continent must be greater than sum of it's countries population")
            else:
                print("Validation ok: population of this continent is equal or greater than sum of it's countries population")
        else:
            print("Validation: No entries on data base to validate population and area values")





    def createNewCountry(self, _name, _continent, _population, _area, _hospitals, _national_parks, _rivers, _schools):
        new_country = Country(name = _name, continent = _continent, population = _population, area = _area, hospitals = _hospitals, \
                                national_parks = _national_parks, rivers = _rivers, schools = _schools)
        self.session.add(new_country)
        self.session.commit()
        print ("Country '%s' added to db"% _name)

    def updateCountry(self, _name, _continent, _population, _area, _hospitals, _national_parks, _rivers, _schools):
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
        return ("Country '%s' updated"% _name)


    def deleteCountry(self, _name):
        country = self.session.query(Country).filter_by(name = _name).one()
        self.session.delete(country)
        self.session.commit()
        return ("Country '%s' deleted"% _name)

    def countryExists(self, _name):
        # print 'debug: country exists function'
        if self.session.query(exists().where(Country.name == _name)).scalar():
            return True
    
    