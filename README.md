# Hotel management system

API allows to make reservations with overbooking for guests of hotel

## Concept 

The API is created with Django REST Framework - add-on for Django framework.
Database - Postgres

Project uses Docker and Docker compose and can be run 
in local developer's environment and remote hosting as well.

## Endpoints

### Configuration
Resource for managing configuration parameters. Parameters are stored in DB as a history.
When it is needed, system gets the latest value of parameter according to the date of change.

There are next methods:
- list (get list of all parameters with their types)
- retrieve (get the value of specified parameter)
- update (updates the value of parameter)

### Reservation
There is special endpoint for add new reservation using guest name and email and the range of dates (arrival, departure)
System checks the possibility of reservation for the specified range of days, and if at least one day is overbooked, the system denied the reservation with error '400 Bad request'

## Running the server
You need Docker, docker-compose and make utility installed on your computer.
For running initial database creation, use command:

$ make init

Than you need to create super-user for accessing administration panel:

$ make create-user

and follow the dialog to create user

Now you can run the project. Use command:

$ make run

### Running tests

To run tests, use command:

$ make tests

### Accessing to API documentation

Type in the browser http://127.0.0.1:8000/docs/ to see the API endpoints

### Changing the port

By default the project occupies port 8000. But if you have a reason to use another port, you can change it in the docker-compose.yaml file.

There is section 'ports' of 'web' service. Change the first number in this section (for example, 8001:8000)