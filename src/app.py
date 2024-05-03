import json

from db import db
from flask import Flask, request

from db import Post
from db import Category

app = Flask(__name__)
db_filename = "cms.db"

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
    Endpoint for deleting a course by its id
    """
    category = Category.query.filter_by(id=category_id).first()
    if category is None:
        return failure_response("category not found")
    db.session.delete(category)
    db.session.commit()
    return success_response(category.serialize())


# --POST ROUTES ---------------------------------------------------------------

@app.route("/api/posts/", methods = ["POST"])
def create_post():
    """
    Endpoint for creating a to-do post
    """
    body = json.loads(request.data)
    if body == None:
        return failure_response("Empty request!", 400)
    title = body.get("title")
    dueDate = body.get("dueDate")
    if (title == None or dueDate == None):
        return failure_response("Incomplete request!", 400)
    if (type(title) is not str or type(dueDate) is not str):
        return failure_response("Wrong data type! Require strings", 400)
    new_post = Post(title = title, dueDate = dueDate)
    db.session.add(new_post)
    db.session.commit()
    return success_response(new_post.serialize(), 201)

@app.route("/api/posts/<int:post_id>/")
def get_post_by_id(post_id):
    """
    Endpoint for getting a specific Post by its id
    """
    post = Post.query.filter_by(id=post_id).first()
    if post is None:
        return failure_response("Post not found")
    return success_response(post.serialize())

@app.route("/api/posts/<int:post_id>/add/", methods = ["POST"])
def add_post_to_category(category_id):
    """
    Endpoint for adding a user to a course
    """
    body = json.loads(request.data)
    if body is None:
        return failure_response("Empty request", 400)
    user_id = body.get("user_id")
    user_type = body.get("type")
    if (user_id == None or user_type == None):
        return failure_response("Incomplete request", 400)
    if (type(user_id) is not int or type(user_type) is not str):
        return failure_response("Wrong data type", 400)

    category = Category.query.filter_by(id=category_id).first()
    if category is None:
        return failure_response("category not found")
    post = Post.query.filter_by(id=user_id).first()
    if post is None:
        return failure_response("post not found")
    category.append(post)
    db.session.commit()
    
    return success_response(category.serialize())

@app.route("/api/posts/<int:post_id>/", methods = ["DELETE"])
def delete_post(post_id):
    """
    Endpoint for deleting a post by its id
    """
    post = Post.query.filter_by(id=post_id).first()
    if post is None:
        return failure_response("Post not found")
    db.session.delete(post)
    db.session.commit()
    return success_response(post.serialize())

