# Solution for the Wolt Summer 2024 Engineering Internships backend assignment.

## Delivery Fee Calculator API

This repository contains my solution for the Wolt Summer 2024 Engineering Internship backend assignment. The application is written with Python (3.10.12), using FastAPI library. The API is fully configurable and tested with 96% test coverage, where the last 4% are trivial in terms of the function of the program. All inputs and outputs are validated to avoid errors in other apps that depend on this API.

### Requirements

- Python version 3.10.12 or higher

- pip version 22.0.2 or higher

### Development practices used:

- Dependency management: [venv](https://docs.python.org/3/library/venv.html) was used to create virtual environment and dependency list was saved to requirements.txt.

- Testing: Unit- and integration tests were created with pytest and they test the API via FastAPI's test client feature.

- Configuration: No constants are used within the classes or functions, rather they are written in separate file, from which they are imported. This improves the application's maintainability. Tests are not dependent on the config file, so they won't break if constants are changed. Config file is validated before the program is run to avoid internal server errors caused by mistakes in config file.

- Error handling: Custom errors were created with relevant messages if request body is not valid.

- Documentation: Docstring and comments are used when needed and code is written with readability in mind.

- Ease of use: Scripts for both starting the app and running automated tests.

- Github workflow: On every push, tests are run to check health of the application.

### How to use

Quick start: install needed dependencies and run the server with a provided script: 

```start.sh```

Or manually:

- Install requirements by runnin ```pip install -r requirements.txt```

- Run the server by running the ```main.py```

The API is now open at http://localhost:8000/

### Testing

Run tests with ```test.sh```

This will generate a coverage report as well.

### Configuration

- You can configure the application in the config.py file.

- There is a separate test_config.py file for testing, so changes in development/production configuration file won't break the tests.

- Configuration is validated, and if there are errors, the server won't start.

### Usage Demo
#### Correct request body
The client sends a POST request with a JSON request body: 

```
Content-Type: application/json
{"cart_value": 790, "delivery_distance": 2235, "number_of_items": 4, "time": "2024-01-15T13:00:00Z"}
```

Server responds with:
```
HTTP/1.1 200 OK
date: Wed, 31 Jan 2024 10:51:49 GMT
server: uvicorn
content-length: 20
content-type: application/json
Connection: close

{
  "delivery_fee": 710
}
```
#### Incorrect request body
The client sends a POST request with a JSON request body with a time format that is not ISO 8601
```
Content-Type: application/json

{"cart_value": 790, "delivery_distance": 2235, "number_of_items": 4, "time": "2024-01-01 12:00:00"}
```
Server responds with:
```
HTTP/1.1 400 Bad Request
date: Wed, 31 Jan 2024 10:53:43 GMT
server: uvicorn
content-length: 51
content-type: application/json
Connection: close

"Time must be string type in UTC, ISO 8601 format."
```