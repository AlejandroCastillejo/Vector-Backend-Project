# Vector Backend Engineering Project

This project implement the entire stack of a simple backend application

### Dependencies
The code in this repository require the following libraries to be installed:
* Flask
* SQLAlchemy
* Zookeeper and Kafka
* kafka-python
<br/>

## Part 1
Part 1 is composed of two files:
* *models.py*   which defines 3 table models: Continents, Countries and Cities.
* *writer.py*   which create, update and delete database values.

Continents table, e.g., has 4 columns: 'name', 'id', 'population' and 'area'.
By calling the method POST at route '/continents', *writer.py* creates a new entry in this table. But first, it checks that 'name' param is not empty and also that this row doesn't already exist. I boot cases it returns and error message.

## Part 2
For part 2 the "writer" script has been modified and divided into 2:
* *db_manager:* define dbManager class which methods post, update or delete entries in the data base.
* *writer_for_broker*: some of the functions from *writer.py* have been updated to work as "consumers" of Kafka broker instead of Flask app functions.

*client.py:* this script work as "producer" for Kafka broker. Publish some 'topics' with the information of http requests from FLask app

### Test the aplication so far

* Launch Zookeeper and Kafka
* Add to Kafka the topics: 'continent' and 'country'
* Run both python scripts: *client.py* and *writer_for_broker.py*
* Send http requests to http://0.0.0.0:5000/continent and http://0.0.0.0:5000/country using PUT, POST or DELETE methods.
(For more details about acepted arguments see *models.py*)

<br/>

**Potential improvement:** add RecordMetadata functionalities to *client.py*
