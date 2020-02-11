from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine

Base = declarative_base()


class Continent(Base):
    __tablename__ = 'continents'

    name = Column(String(14), nullable = False) #longest continent name has 13 characters
    id = Column(Integer, primary_key = True)
    population = Column(Integer)
    area = Column(Integer)

    @property
    def serialize(self):
       """Return object data in easily serializeable format"""
       return {
       		    'id': self.id,
                'name': self.name,
                'population' : self.population,
                'area' : self.area
            }

class Country(Base):
    __tablename__ = 'countries'

    name = Column(String(40), nullable = False) #let's suppose the longest name has no mere than 40 characters
    id = Column(Integer, primary_key = True)
    continent = Column(String(14))
    population = Column(Integer)
    area = Column(Integer)
    hospitals = Column(Integer)
    national_parks = Column(Integer)
    rivers = Column(Integer)
    schools = Column(Integer)

    @property
    def serialize(self):
       return {
       		    'id': self.id,
                'name': self.name,
                'continent': self.continent,
                'population' : self.population,
                'hospitals' : self.hospitals,
                'national_parks' : self.national_parks,
                'rivers' : self.rivers,
                'schools' : self.schools
            }

class City(Base):
    __tablename__ = 'cities'

    name = Column(String(40), nullable = False) #same
    id = Column(Integer, primary_key = True)
    country = Column(String(40))
    population = Column(Integer)
    area = Column(Integer)
    roads = Column(Integer)
    trees = Column(Integer)
    shops = Column(Integer)
    schools = Column(Integer)

    @property
    def serialize(self):
       return {
       		    'id': self.id,
                'name': self.name,
                'country': self.country,
                'population' : self.population,
                'area' : self.area,
                'roads' : self.roads,
                'trees' : self.trees,
                'shops' : self.shops,
                'schools' : self.schools
            }


# Create engine and tables
engine = create_engine('sqlite:///backend_project.db')
Base.metadata.create_all(engine)