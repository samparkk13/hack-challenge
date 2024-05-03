from multiprocessing.sharedctypes import Value
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Post(db.Model):
    """
    Posts Class
    """
    __tablename__ = "posts"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    dueDate = db.Column(db.String, nullable=False)
    category = db.Column(db.String, nullable=False)
    finished = db.Column(db.Boolean, nullable=False)

    def __init__(self, **kwargs):
        """
        Initialize a post
        """
        self.id = kwargs.get("id")
        self.title = kwargs.get("title")
        self.finished = kwargs.get("finished", False)
        self.dueDate = kwargs.get("dueDate", "00/00/0000")
        self.category = kwargs.get("category")

    def serialize(self):
        """
        Serialize a post
        """
        return {
            "id": self.id,
            "title": self.title,
            "finished": self.finished,
            "dueDate": self.dueDate,
            "category": self.category,
        }


class Category(db.Model):
    """
    Category Class
    """

    __tablename__ = "category"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    finished = db.Column(db.Boolean, nullable=False)
    task_id = db.Column(db.Integer, db.ForeignKey("task.id"), nullable=False)

    def __init__(self, **kwargs):
        """
        Initialize a post description
        """
        self.id = kwargs.get("id")
        self.title = kwargs.get("title")
        self.finished = kwargs.get("finished", False)
        self.task_id = kwargs.get("task_id")

    def serialize(self):
        """
        Serialize a post description
        """
        return {
            "id": self.id,
            "title": self.title,
            "finished": self.finished,
            "task_id": self.task_id,
        }