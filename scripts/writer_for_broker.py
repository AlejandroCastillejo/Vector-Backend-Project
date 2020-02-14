from kafka import KafkaConsumer
from json import loads
from db_manager import dbManager

db = dbManager()   #crete object of dbManager class

consumer = KafkaConsumer(
    *['continent', 'country', 'city'],
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

# @app.route("/continent", methods = ['POST', 'PUT', 'DELETE'])
def continentsFunction(_message):
    req_method = _message.value['method']
    print ('req_method: ', req_method)

    continent_args = ['name', 'population', 'area']
    for arg in continent_args:
        try:
            exec("%s = _message.value['args']['%s']"% (arg, arg))
        except KeyError:
            exec("%s = ''"% arg)

    # Call this method to create a new continent
    if req_method == 'POST':
        if name == '':
            print ("Error: 'name' param can't be empty")
            # return ("Error: 'name' param can't be empty")
        elif db.continentExists(name):
            print ("Error: '%s' entry already exists on 'continents' table. Please use PUT method to update it"% name)
            # return ("Error: '%s' entry already exists on 'continents' table. Please use PUT method to update it"% name)
        else:
            return db.createNewContinent(name, population, area)
            print (name, "added to 'continents' table")

    #Call this method to update a specific continent
    if req_method == 'PUT':
        if db.continentExists(name):
            return db.updateContinent(name, population, area)
        else:
            print ("Error: '%s' entry does not exists on 'continents' table. Please use POST method to create it"% name)
            # return ("Error: '%s' entry does not exists on 'continents' table. Please use POST method to create it"% name)

    #Call this method to delelte a continent
    elif req_method == 'DELETE':
        if db.continentExists(name):
            return db.deleteContinent(name)
        else:
            print ("Error: '%s' entry cannot be deleted. It does not exists on 'continents' table."% name)
            # return ("Error: '%s' entry cannot be deleted. It does not exists on 'continents' table."% name)


# @app.route("/country", methods = ['POST', 'PUT', 'DELETE'])
def countriesFunction(_message):
    req_method = _message.value['method']
    print ('req_method: ', req_method)

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
            print ("Error: 'name' param can't be empty")
            # return ("Error: 'name' param can't be empty")
        elif db.countryExists(name):
        # elif db.
            print ("Error: '%s' entry already exists on 'countries' table. Please use PUT method to update it"% name)
            # return ("Error: '%s' entry already exists on 'countries' table. Please use PUT method to update it"% name)
        else:
            return db.createNewCountry(name, continent, population, area, hospitals, national_parks, rivers, schools) 
            print (name, "added to 'countries' table")

    #Call this method to update a specific country
    if req_method == 'PUT':
        if db.countryExists(name):
            return db.updateCountry(name, continent, population, area, hospitals, national_parks, rivers, schools)
        else:
            print ("Error: '%s' entry does not exists on 'countries' table. Please use POST method to create it"% name)
            # return ("Error: '%s' entry does not exists on 'countries' table. Please use POST method to create it"% name)

    #Call this method to delelte a country
    elif req_method == 'DELETE':
        if db.countryExists(name):
            return db.deleteCountry(name)
        else:
            print ("Error: '%s' entry cannot be deleted. It does not exists on 'countries' table."% name)
            # return ("Error: '%s' entry cannot be deleted. It does not exists on 'countries' table."% name)


if __name__ == '__main__':
    print ("Writer for broker running")
    runKafkaConsumer()