import os
import sys
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random
from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)

    """
    @TODO: Set up CORS. Allow '*' for origins. Delete the sample route after completing the TODOs
    """
    cors = CORS(app, resources = {r"/api/*":{"origins": "*"}})


    """
    @TODO: Use the after_request decorator to set Access-Control-Allow
    """
    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Headers',
                            'Content-Type, Authorization, true')
        response.headers.add('Access-Control-Allow-Methods',
                            'GET, PATCH, POST, DELETE, OPTIONS')
        return response

# pagination helper method
    def paginate_questions(request, selection):
# argument of 'request' to get the page number; if none is included, default to 1
        page = request.args.get('page', 1, type=int)
        start = (page - 1) * QUESTIONS_PER_PAGE
        end = start + QUESTIONS_PER_PAGE

        questions = [question.format() for question in selection]
        current_questions = questions[start:end]

        return current_questions


    """
    @TODO:
    Create an endpoint to handle GET requests
    for all available categories.
    """
# app.route('/) automatically defaults to GET, thus the method must not be necessarily specified here. 
    @app.route('/categories')
    def retrieve_categories():
        categories = Category.query.all()

        categories_retrieved = {}
        for category in categories:
            categories_retrieved[category.id] = category.type

        if not categories:
            abort(404)

        return jsonify({
        'success': True,
        'categories' : categories_retrieved
        })           



    """
    @TODO:
    Create an endpoint to handle GET requests for questions,
    including pagination (every 10 questions).
    This endpoint should return a list of questions,
    number of total questions, current category, categories. """

    @app.route('/questions')
    def get_questions():
        selection = Question.query.order_by(Question.id).all()
        current_questions = paginate_questions(request, selection)

        if len(current_questions) == 0:
            abort(404)

        categories = Category.query.all()
        categories_retrieved = {}
        for category in categories:
            categories_retrieved[category.id] = category.type

        return jsonify({
            'success': True,
            'questions': current_questions,
            'total_questions': len(selection),
            'categories' : categories_retrieved,
            'current_category' : None
            })


    """
    # @TODO:
    # Create an endpoint to DELETE question using a question ID.
    # """
    
    @app.route('/questions/<int:question_id>', methods=['DELETE'])
    def delete_question(question_id):
        try:
            question = Question.query.filter(Question.id == question_id).one_or_none()
            if question is None:
                abort(404)

    #  delete question           
            question.delete()
    #  send back remaining books to update the frontend       
            selection = Question.query.order_by(Question.id).all()
            current_questions = paginate_questions(request, selection)

            return jsonify({
                'success': True,
                'deleted': question_id,
                'questions': current_questions,
                'total_questions': len(Question.query.all())
            })
        except:
            # print(sys.exec_info())
            abort(422)
        

    """
    @TODO:
    Create an endpoint to POST a new question,
    which will require the question and answer text,
    category, and difficulty score.
    """

    @app.route('/questions', methods=['POST'])
    def add_question():
        body = request.get_json()

    # New Data
        new_question = body.get('question', None)
        new_answer = body.get('answer', None)
        new_category = body.get('category', None)
        new_difficulty = body.get('difficulty', None)
        # search_term = body.get('searchTerm', None)

        try:
            question = Question(question=new_question, answer=new_answer, 
            category=new_category, difficulty=new_difficulty)
    # insert question into database
            question.insert()

            selection = Question.query.order_by(Question.id).all()
            current_questions = paginate_questions(request, selection)

            return jsonify({
                'success': True,
                'added': question.id,
                'questions': current_questions,
                'total_questions': len(Question.query.all())
            })
        except:
            abort(422)
            # print(sys.exec_info())



    """
    @TODO:
    Create a POST endpoint to get questions based on a search term.
    It should return any questions for whom the search term
    is a substring of the question.

    """ 

    @app.route("/questions/search", methods=['POST'])
    def search_for_questions():
        body = request.get_json()
        search_string = body.get("searchTerm", None)

        try:
            if search_string == '':
                questions = Question.query.all()
            else:
                questions = Question.query.filter(Question.question.ilike(f'%{search_string}%')).all()
                current_questions = paginate_questions(request, questions)
                if current_questions == None:
                    abort(404)
                return jsonify({
                    "success": True,
                    "questions": current_questions,
                    "total_questions": len(questions)
                })
          
        except:
            abort(404)
            # print(sys.exc_info())


    """
    @TODO:
    Create a GET endpoint to get questions based on category.

    """
    @app.route('/categories/<int:id>/questions')
    def get_questions_by_categories(id):

        category = Category.query.filter_by(id=id).one_or_none()
        if category:
            selection = (Question.query.filter(Question.category == id)
            .order_by(Question.id).all())

            current_questions = paginate_questions(request, selection)

            return jsonify({
            'success': True,
            'questions': current_questions,
            'total_questions': len(selection),
            'current_category' : category.type
            })
        else:
            abort(404)


    """
    @TODO:
    Create a POST endpoint to get questions to play the quiz.
    This endpoint should take category and previous question parameters
    and return a random questions within the given category,
    if provided, and that is not one of the previous questions.

    """

    @app.route('/quizzes', methods=['POST'])
    def play_game():
        body = request.get_json()
        used_questions = body.get('previous_questions')
        category = body.get('quiz_category')
        try:
            questions = Question.query.filter_by(category=int(category['id'])).all()
            current_question = None

            while current_question is None:
                 random_num = random.randint(0, len(questions)-1)
                 if questions[random_num].id not in used_questions:
                    current_question = questions[random_num]
                    break
            return jsonify({
                'question': current_question.format()
            })
        except:
            abort(404)


    """
    @TODO:
    Create error handlers for all expected errors
    including 404 and 422.
    """
    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
                "success": False, 
                "error": 400, 
                "message": "bad request"
                }
            ), 400

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
                "success": False,
                "error": 404,
                "message": "not found"
            }
        ), 404

    @app.errorhandler(405)
    def method_not_allowed(error):
        return jsonify({
                "success": False,
                "error": 405,
                "message": "method not allowed"
            }
        ), 405

    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
                "success": False, 
                "error": 422, 
                "message": "unprocessable"
                }
            ), 422

    @app.errorhandler(500)
    def internal_server_error(error):
        return jsonify({
                "success": False,
                "error": 500,
                "message": "internal server error"
            }
        ), 500

    return app 