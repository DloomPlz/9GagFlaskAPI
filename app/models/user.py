from .. import db
from flask import current_app
from itsdangerous import (TimedJSONWebSignatureSerializer
                          as Serializer, BadSignature, SignatureExpired)



# many to many entre 2 models différents
upvote_post =   db.Table('upvote_post',
                    db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True),
                    db.Column('post_id', db.Integer, db.ForeignKey('post.id'), primary_key=True)
)


# many to many entre 2 models différents
upvote_comment =   db.Table('upvote_comment',
                    db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True),
                    db.Column('comment_id', db.Integer, db.ForeignKey('comment.id'), primary_key=True)
)

class User(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, nullable=False, unique=True)
    email = db.Column(db.String, nullable=False, unique=True)
    password = db.Column(db.String, nullable=False)

    # one to many -> se retrouve grâce à la clef etrangère dans le model Post
    posts = db.relationship("Post", backref="user", cascade="all, delete-orphan")

    # one to many -> se retrouve grâce à la clef etrangère dans le model Post
    comments = db.relationship("Comment", backref="user", cascade="all, delete-orphan")

    # many to many models différents
    upvoted_comments = db.relationship("Comment",
                        secondary=upvote_comment,
                        backref=db.backref(
                            "upvoted_by",
                            lazy="dynamic"
                        )
                    )

     # many to many models différents
    upvoted_posts = db.relationship("Post",
                        secondary=upvote_post,
                        backref=db.backref(
                            "upvoted_by",
                            lazy="dynamic"
                        )
                    )
    def generate_auth_token(self, expiration = 172800):
        s = Serializer(current_app.config.get('SECRET_KEY'), expires_in = expiration)
        return s.dumps({ 'id': self.id })
