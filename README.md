# Solution for the Wolt Summer 2024 Engineering Internships backend assignment.

## Delivery Fee Calculator API

This repository contains my solution for the Wolt Summer 2024 Engineering Internship backend assignment. The application is written with Python (3.10.12), using FastAPI library. The API is fully configurable and tested with 100% test coverage. All inputs and outputs are validated to avoid errors in other apps that depend on this API.

Development practices used:

- Dependency management: [venv](https://docs.python.org/3/library/venv.html) was used to create virtual environment and dependency list was saved to requirements.txt.

- Testing: Tests were created with pytest and they test the API via FastAPI's test client feature.

- Configuration: No constants are used within the classes or function, rather they are written in separate file, from which they are imported. This improves the application's maintainability.

- Documentation: Docstring and comments are used when needed and code is written with readability in mind.

- Ease of use: Scripts for both starting the app and running automated tests.

- Github workflow: On every push, tests are run to check health of the application.

### How to use

Quick start: install needed dependencies and run the server with a provided script: 

```start.sh```

Or manually:

- Install requirements by runnin ```pip install -r requirements.txt```

- Run the server in src folder with ```uvicorn main:app```

The API is now open at http://localhost:8000/

### Testing

Run tests with ```test.sh```

This will generate a coverage report as well.

### Configuration

- You can configure the application in the config.py file

## The Assignment

## Delivery Fee Calculator

The goal of the assignment is to showcase your coding skills and ability to develop features. This is a highly important part of the hiring process so it's crucial to put effort into this without making it too bloated. Reviewers will put weight on three main aspects: code quality, maintainability, and testing. Based on the results of the assignment review, we will make the decision on proceeding to the technical interview.

Your task is to write a delivery fee calculator. This code is needed when a customer is ready with their shopping cart and we’d like to show them how much the delivery will cost. The delivery price depends on the cart value, the number of items in the cart, the time of the order, and the delivery distance.


### Specification
Rules for calculating a delivery fee
* If the cart value is less than 10€, a small order surcharge is added to the delivery price. The surcharge is the difference between the cart value and 10€. For example if the cart value is 8.90€, the surcharge will be 1.10€.
* A delivery fee for the first 1000 meters (=1km) is 2€. If the delivery distance is longer than that, 1€ is added for every additional 500 meters that the courier needs to travel before reaching the destination. Even if the distance would be shorter than 500 meters, the minimum fee is always 1€.
  * Example 1: If the delivery distance is 1499 meters, the delivery fee is: 2€ base fee + 1€ for the additional 500 m => 3€
  * Example 2: If the delivery distance is 1500 meters, the delivery fee is: 2€ base fee + 1€ for the additional 500 m => 3€
  * Example 3: If the delivery distance is 1501 meters, the delivery fee is: 2€ base fee + 1€ for the first 500 m + 1€ for the second 500 m => 4€
* If the number of items is five or more, an additional 50 cent surcharge is added for each item above and including the fifth item. An extra "bulk" fee applies for more than 12 items of 1,20€
  * Example 1: If the number of items is 4, no extra surcharge
  * Example 2: If the number of items is 5, 50 cents surcharge is added
  * Example 3: If the number of items is 10, 3€ surcharge (6 x 50 cents) is added
  * Example 4: If the number of items is 13, 5,70€ surcharge is added ((9 * 50 cents) + 1,20€)
  * Example 5: If the number of items is 14, 6,20€ surcharge is added ((10 * 50 cents) + 1,20€)
* The delivery fee can __never__ be more than 15€, including possible surcharges.
* The delivery is free (0€) when the cart value is equal or more than 200€. 
* During the Friday rush, 3 - 7 PM, the delivery fee (the total fee including possible surcharges) will be multiplied by 1.2x. However, the fee still cannot be more than the max (15€). Considering timezone, for simplicity, **use UTC as a timezone in backend solutions** (so Friday rush is 3 - 7 PM UTC). **In frontend solutions, use the timezone of the browser** (so Friday rush is 3 - 7 PM in the timezone of the browser).

### Expectations
When reviewing your code, we will focus on the part that fulfils the requirements explained above. We would love to see a well-tested and readable solution.

Pro tip: When you think you are ready with the assignment, take at least a few hours break, and then go through the code one more time before returning it.

### Submitting the assignment
Bundle everything into a Zip archive and upload it to Google Drive, Dropbox or similar and include the link in the application. Remember to check permissions! If we cannot access the file, we cannot review your code. Please don’t store your solution in a public GitHub repository during the application period.

A good check before sending your task is to unzip the Zip archive into a new folder and check that building and running the project works, using the steps you define in readme.md. Forgotten dependencies and instructions can sometimes happen even to the best of us.

## Backend specifics

### Your task
Your task is to build an HTTP API which could be used for calculating the delivery fee.

Please use one of the programming languages available in the location you're applying to (Helsinki: Python / Kotlin & Berlin: Python / Kotlin / Scala). Feel free to use libraries / frameworks.

**Note that your technology choice here defines the scope of the possible technical interview and your focus area if starting to work at Wolt 😊**


### Specification
Implement an HTTP API (single POST endpoint) which calculates the delivery fee based on the information in the request payload (JSON) and includes the calculated delivery fee in the response payload (JSON).

#### Request
Example: 
```json
{"cart_value": 790, "delivery_distance": 2235, "number_of_items": 4, "time": "2024-01-15T13:00:00Z"}
```

##### Field details

| Field             | Type  | Description                                                               | Example value                             |
|:---               |:---   |:---                                                                       |:---                                       |
|cart_value         |Integer|Value of the shopping cart __in cents__.                                   |__790__ (790 cents = 7.90€)                |
|delivery_distance  |Integer|The distance between the store and customer’s location __in meters__.      |__2235__ (2235 meters = 2.235 km)          |
|number_of_items    |Integer|The __number of items__ in the customer's shopping cart.                   |__4__ (customer has 4 items in the cart)   |
|time               |String |Order time in UTC in [ISO format](https://en.wikipedia.org/wiki/ISO_8601). |__2024-01-15T13:00:00Z__                   |

#### Response
Example:
```json
{"delivery_fee": 710}
```

##### Field details

| Field         | Type  | Description                           | Example value             |
|:---           |:---   |:---                                   |:---                       |
|delivery_fee   |Integer|Calculated delivery fee __in cents__.  |__710__ (710 cents = 7.10€)|