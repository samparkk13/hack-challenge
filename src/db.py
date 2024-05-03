from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Category(db.Model):
    """
    Category Class
    """

    __tablename__ = "categories"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String, nullable=False)    
    todos = db.relationship("Todo", cascade = "delete")
    
   

    def __init__(self, **kwargs):
        """
        Initialize a post description
        """
        self.title = kwargs.get("title", "")


    def serialize(self):
        """
        Serialize a post description
        """
        todos = [
            {
                "id": todo.id,
                "title": todo.title,
                "due_date": todo.due_date
            }
            for todo in self.todos
        ]
        return {
            "id": self.id,
            "title": self.title,
            "todo": todos
        }


class Todo(db.Model):
    """
    Todo Class
    """
    __tablename__ = "todo"
    id = db.Column(db.Integer, primary_key = True, auto_increment = True)
    title = db.Column(db.String, nullable = False)
    due_date = db.Column(db.Integer, nullable = False)
    category_id = db.Column(db.Integer, db.ForeignKey("categories.id"), nullable = False)

    def __init__(self, **kwargs):
        """
        Initialize a Todo object
        """
        self.title = kwargs.get("title", "")
        self.due_date = kwargs.get("due_date", 0)
        self.category_id = kwargs.get("category_id", 0)
    
    def serialize(self):
        """
        Serialize an Todo object
        """
        category = Category.query.filter_by(id=self.category_id).first()

        return {
        "id": self.id,
        "title": self.title,
        "due_date": self.due_date,
        "category": category.title,
        }