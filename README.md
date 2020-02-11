# Vector Backend Engineering Project

This project implement the entire stack of a simple backend application

### Dependencies
The code in this repository require the following libraries to be installed:
* Flask
* SQLAlchemy
<br/>

## Part 1
Part 1 is composed of two files:
* *models.py*   which defines 3 table models: Continents, Countries and Cities.
* *writer.py*   which create, update and delete database values.

Continents table, e.g., has 4 columns: 'name', 'id', 'population' and 'area'.
By calling the method POST at route '/continents', *writer.py* creates a new entry in this table. But first, it checks that 'name' param is not empty and also that this row doesn't already exist. I boot cases it returns and error message.