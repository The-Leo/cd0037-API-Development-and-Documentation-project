## BACKEND PROJECT DOCUMENTATION FOR TRIVIA API

Contents: 
# Backend - Trivia API

## Setting up the Backend

### Install Dependencies

#### API Documentation

1. **Python Version** This project was completed using Python3: 3.10.5 version

Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

2. **Virtual Environment** - Project was executed in the virtual environment to keep the dependencies separate and organized. But for the purpose of submission, to reduce the number of files, the virtual environment folder was deleted. 

Instructions for setting up a virual environment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

3. **PIP Dependencies** - Once the virtual environment was setup and running, the required dependencies were installed by navigating to the `/backend` directory and running:

```bash
pip install -r requirements.txt
```
psycopg2 did not integrate smoothly, so it was installed independently. 

#### Key Pip Dependencies

- [Flask](http://flask.pocoo.org/) is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM used to handle the lightweight SQL database. 

- [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#) is the extension used to handle cross-origin requests from our frontend server.

### Database Setup

With Postgres running, a database was created and named `trivia`. 

```bash
createdb trivia
```

The database was populated using the `trivia.psql` file provided. In the psql shell, run:

'''\i filepath/trivia.psql'''

The username of the database was changed from student to postgres to allow for smooth integration. 


### Run the Server
Ensure you are working within the virtual environment and Within the backend directory. To run the server, execute:

export FLASK_APP=flaskr
export FLASK_DEBUG=true
flask run


flask-CORS was used to enable cross-domain requests and used to set response headers. 


## API DOCUMENTATION
The following section provides detailed documentation of the API endpoints including the URL, request parameters, and the response body.

Within the flaskr directory (in the backend parent directory) is the __init__.py file, which contains the endpoints. 

Protocol:
Requests sent to the server were through the HTTP Protocol, with their corresponding Request Methods. The server was hosted locally through port 5000. 

Methods:
Methods enabled by CORS are:
[GET, PATCH, POST, DELETE, OPTIONS]
Three of these methods were utilized in the project: GET, POST and DELETE. 


Error Handling:
Http Error Responses
400 - Bad Request
404 - Not Found
405 - Method Not Allowed
422 - Unprocessable
500 - Internal Server Error

Errors have a json format. Sample Error Handler: 
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
                "success": False,
                "error": 404,
                "message": "not found"}), 404

Endpoint URLs:

GET '/categories'
GET '/questions'
DELETE '/questions/id'
POST '/questions'
POST '/questions/search'
GET '/categories/id/questions'
POST '/quizzes'

## GET '/categories'
This Endpoint handles GET requests for all available categories.

  "categories": {
    "1": "Science",
    "2": "Art",
    "3": "Geography",
    "4": "History",
    "5": "Entertainment",
    "6": "Sports"},

Testing Endpoint with curl:
curl http://127.0.0.1:5000/categories 

## GET '/questions'
This end point handles GET requests for questions, including pagination (every 10 questions).
This endpoint returns a list of questions, number of total questions, current category, categories. 
Sample Questions:
    {"answer": "George Washington Carver",
      "category": 4,
      "difficulty": 2,
      "id": 12,
      "question": "Who invented Peanut Butter?"},

    { "answer": "Lake Victoria",
      "category": 3,
      "difficulty": 2,
      "id": 13,
      "question": "What is the largest lake in Africa?"}
  "success": true,
  "total_questions": ...

Testing Endpoint with Curl:
curl http://127.0.0.1:5000/questions


## DELETE '/questions/id'
This endpoint deletes question using a question ID.

Testing Endpoint with Curl:
curl -X DELETE http://127.0.0.1:5000/questions/8 

## POST '/questions'
This endpoint posts a new question, with the question and answer text, category, and difficulty score.

Testing Endpoint with Curl:
curl -X POST -H "Content-Type: application/json" -d '{"question":"What is the scariest day of the year?", "answer":"Halloween", "difficulty":"3", "id":"12"}' http://127.0.0.1:5000/questions

## POST '/questions/search'
This endpoint creates gets questions based on a search term. It returns any question for whom the search term is a substring of the question. 

Testing endpoint with Curl:
curl http://127.0.0.1:5000/questions -X POST -H "Content-Type: application/json" -d '{"searchTerm": "title"}'

## GET '/categories/id/questions'
This endpoint creates or fetches questions based on category.

## POST '/quizzes'
This endpoint gets questions to play the quiz. This endpoint takes category and previous question parameters and returns a random question within the given category, if provided, and that is not one of the previous questions.

Testing with Curl:
curl -X POST -H "Content-Type: application/json" -d '{"previous_questions": [12], "quiz_category": {"type": "History", "id": "1"}}' http://127.0.0.1:5000/quizzes

## Testing

Write at least one test for the success and at least one error behavior of each endpoint using the unittest library.

To deploy the tests, run

```bash
dropdb trivia_test
createdb trivia_test
psql trivia_test < trivia.psql
python test_flaskr.py
```
