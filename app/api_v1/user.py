from flask import jsonify, request, current_app
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



############ CREER NEW USER ---- WORKS

@api.route('/users/signup', methods=['POST'])
def signup_user():
    datas = request.get_json()
    username=datas.get('username','')

    # TESTS

    if username is '':
        return jsonify(error="username is empty"),400
    email=datas.get('email','')
    if email is '':
        return jsonify(error="email is empty"),400
    password=datas.get('password','')
    if password is '':
        return jsonify(error="password is empty"),400

    u = User()
    u.username = username
    u.email = email
    u.password = bcrypt.generate_password_hash(password)

    if User.query.filter(User.username.ilike(username)).first() is not None:
        return jsonify(error="Username taken"),400
    db.session.add(u)
    db.session.commit()
    token = u.generate_auth_token().decode('ascii')
    return jsonify(token=token),200


############## LOGIN PAR USER OU MAIL  -----WORKS

@api.route('/users/login', methods=['POST'])
def login_username_or_email():
    datas = request.get_json()

    # Récupération des datas et tests
    password=datas.get('password','')
    if password is '':
        return jsonify(error="password is empty"),400

    username=datas.get('username','')
    if username is '':
        return jsonify(error="username is empty"),400

    # connexion via username
    user = User.query.filter(User.username.ilike(username)).first()
    if user is not None:
        if bcrypt.check_password_hash(user.password, password):
            token = user.generate_auth_token().decode('ascii')
            return jsonify(token=token),200
        return jsonify(error="username, mail or password is incorrect"),300

    # connexion via email
    email=datas.get('email','')
    if email is '':
        return jsonify(error="email is empty"),400

    user = User.query.filter(User.email.ilike(email)).first()
    if user is not None:
        if bcrypt.check_password_hash(user.password, password):
            token = user.generate_auth_token().decode('ascii')
            return jsonify(token=token),200
    return jsonify(error="username, mail or password is incorrect"),300


######### GETTER USER ---- WORKS


@api.route('/users/<string:username>', methods=['GET'])
def get_user(username):
    user = User.query.filter(User.username == username).first()
    if user is not None:
        return user_schema.jsonify(user),200
    return jsonify(error="user not found"),404


####### DELETE USER


@api.route('/users', methods=['DELETE'])
@authorized
def delete_user(user_id):
    # comme y'a le décorateur authorized, la fonction "delete_user"
    # connait le paramètre 'user_id'
    user = User.query.get(user_id)
    if user is not None:
        if user.id == user_id:
            db.session.delete(user)
            db.session.commit()
            return jsonify(state=True),200
    return jsonify(error="user not found"),404
