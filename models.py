import os
from sqlalchemy import Column
from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()



class Posts(db.Model):
    __tablename__ = 'posts'

    id = Column(db.Integer, primary_key=True)
    image_url = Column(db.String)
    title = Column(db.String(250), nullable=False)
    body = Column(db.Text())
    comments = db.relationship("Comments", cascade="all, delete")
    
    def __init__(self, title, image_url, body):
        self.title = title
        self.image_url = image_url
        self.body = body if body else ""

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def short(self):
        return {
            'id': self.id,
            'title': self.title,
            'image': self.image_url,
            'body': self.body[0:100] + "..."
        }

    def format(self):
        return {
            'id': self.id,
            'title': self.title,
            'image': self.image_url,
            'body': self.body
        }


class Comments(db.Model):
    __tablename__ = 'comments'

    id = Column(db.Integer, primary_key=True)
    title = Column(db.String(250))
    message = Column(db.Text, nullable=False)
    vote = Column(db.Integer, default=0)
    post_id = db.Column(db.Integer, db.ForeignKey('posts.id') , nullable=False)

    def __init__(self, title, message, post_id):
        self.title = title
        self.message = message
        self.post_id = post_id

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def short(self):
        return {
            'id': self.id,
            'message': self.message[0:100] + "..."
        }

    def format(self):
        return {
            'id': self.id,
            'title': self.title,
            'message': self.message,
            'vote': self.vote
        }