from .. import db


class Post(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.String, nullable=False)
    description = db.Column(db.String, nullable=False)
    title = db.Column(db.String, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    # one to many -> se retrouve grâce à la clef etrangère dans le model Post
    comments = db.relationship("Comment", backref="post", cascade="all, delete-orphan")
