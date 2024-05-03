import json

from db import db
from flask import Flask, request

from db import Category
from db import Todo

app = Flask(__name__)
db_filename = "todo.db"

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///%s" % db_filename
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_ECHO"] = True

db.init_app(app)
with app.app_context():
    db.create_all()


# generalized response formats
def success_response(data, code = 200):
    return json.dumps(data), code 

def failure_response(message, code = 404):
    return json.dumps({"error": message}), code

# --CATEGORY ROUTES ------------------------------------------------------------
@app.route("/")
@app.route("/api/categories/") 
def get_categories():
    """
    Endpoint for getting all categories
    """
    categories = []
    for category in Category.query.all():
        categories.append(category.serialize())
    return success_response({"categories": categories})

@app.route("/api/categories/", methods = ["POST"])
def create_category():
    """
    Endpoint for creating a category
    """
    body = json.loads(request.data)
    if body == None:
        return failure_response("Empty request!", 400)
    title = body.get("title")
    if (title == None):
        return failure_response("Incomplete request!", 400)
    if (type(title) is not str):
        return failure_response("Wrong data type! Require strings", 400)
    new_category = Category(title = title)
    db.session.add(new_category)
    db.session.commit()
    return success_response(new_category.serialize(), 201)

@app.route("/api/categories/<int:category_id>/", methods = ["DELETE"])
def delete_category(category_id):
    """
    Endpoint for deleting a category by its id
    """
    category = Category.query.filter_by(id=category_id).first()
    if category is None:
        return failure_response("category not found")
    db.session.delete(category)
    db.session.commit()
    return success_response(category.serialize())


# --TO-DO ROUTES ---------------------------------------------------------------

@app.route("/api/todos/<int:category_id>/create/", methods = ["POST"])
def create_todo_for_category(category_id):
    """
    Endpoint for creating an new todo for a category
    """
    body = json.loads(request.data)
    if body is None:
        return failure_response("Empty request", 400)
    title = body.get("title")
    due_date = body.get("due_date")
    if (title == None or due_date == None):
        return failure_response("Incomplete request", 400)
    if (type(title) is not str or type(due_date) is not str):
        return failure_response("Wrong data type", 400)
    
    category = Category.query.filter_by(id=category_id).first()
    if category is None:
        return failure_response("Category not found")
    new_todo = Todo(title = title, due_date = due_date, category_id = category_id)
    db.session.add(new_todo)
    db.session.commit()
    return success_response(new_todo.serialize(), 201)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)

    
