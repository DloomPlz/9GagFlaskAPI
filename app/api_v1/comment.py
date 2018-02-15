from flask import jsonify, request, current_app, abort

from itsdangerous import (TimedJSONWebSignatureSerializer
                          as Serializer, BadSignature, SignatureExpired)
from functools import wraps

from . import api
from .. import db, bcrypt

from ..models.post import Post
from ..schemas.post import post_schema, posts_schema
from ..models.comment import Comment
from ..schemas.comment import comment_schema, comments_schema
from ..models.user import User
from ..schemas.user import user_schema, users_schema

def authorized(fn):
    @wraps(fn)
    def wrapped(*args, **kwargs):
        if 'Authorization' not in request.headers:
            # Unauthorized
            abort(401)
            return None
        token = request.headers['Authorization'].encode('ascii','ignore')
        s = Serializer(current_app.config.get('SECRET_KEY'), expires_in = 172800)
        try:
            data = s.loads(token)
        except SignatureExpired:
            abort(401)
            return None # valid token, but expired
        except BadSignature:
            abort(401)
            return None # invalid token
        print("user avec id =",data['id'],"a fait une requete.")
        return fn(user_id=data['id'], *args, **kwargs)
    return wrapped


############ CREATE COMMENT

@api.route('/comments', methods=['POST'])
@authorized
def create_comment(user_id):
    datas = request.get_json()

    content = datas.get('content', '')
    if content is '':
        return jsonify(error="content is empty"),400

    post_id = datas.get('post_id', '')
    if post_id is '':
        return jsonify(error="post_id is empty"),400

    comment = Comment()
    comment.content = content
    comment.user_id = user_id
    comment.post_id = post_id

    db.session.add(comment)
    db.session.commit()
    return comment_schema.jsonify(comment),200


######### GETTER COMMENT

@api.route('/comments/<int:comment_id>', methods=['GET'])
def get_comment(comment_id):
    comment = Comment.query.get(comment_id)
    if comment is not None:
        return comment_schema.jsonify(comment),200
    return jsonify(error="comment not found"),404

######## DELETE COMMENT

@api.route('/comments/<int:comment_id>', methods=['DELETE'])
@authorized
def delete_comment(user_id, comment_id):
    # comme y'a le décorateur authorized, la fonction "delete_post"
    # connait le paramètre 'user_id'
    comment = Comment.query.get(comment_id)
    if comment is not None:
        if comment.user_id == user_id:
            db.session.delete(comment)
            db.session.commit()
            return jsonify(state=True),200
        return jsonify(error="This user can't delete this comment!"),401
    return jsonify(error="comment not found"),404

########### UPVOTE COMMENT

@api.route('/comments/<int:comment_id>/upvotes', methods=['POST'])
@authorized
def upvote_comment(user_id, comment_id):
    user = User.query.get(user_id)
    if user is not None:
        comment = Comment.query.get(comment_id)
        if comment is not None:
            #Checker que le comment est pas déja dedans
            if comment not in user.upvoted_comments:
                user.upvoted_comments.append(comment)
                db.session.commit()
                return jsonify(state="ok"),200
            return jsonify(error="comment already upvoted by user"), 403
        return jsonify(error="comment not found"),404
    return jsonify(error="user not found"),404
