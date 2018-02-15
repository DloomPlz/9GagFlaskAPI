from flask import jsonify, request, current_app, abort
from itsdangerous import (TimedJSONWebSignatureSerializer
                          as Serializer, BadSignature, SignatureExpired)
from functools import wraps
from gimgurpython import ImgurClient

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

########## CREATE POST
@api.route('/posts', methods=['POST'])
@authorized
def create_post(user_id):
    datas = request.get_json()

    description=datas.get('description','')
    if description is '':
        return jsonify(error="description not in JSON"),400

    title=datas.get('title','')
    if title is '':
        return jsonify(error="title not in JSON"),400

    image=datas.get('image','')
    if image is '':
        return jsonify(error="image not in JSON"),400
    if image.startswith("data:image/jpeg;base64,"):
        image = image[23:]

    config = {
        'album': None,
        'name':  title,
        'title': title,
        'description': description
    }

    imgur_client = ImgurClient(
        current_app.config['IMGUR_CLIENT_ID'],
        current_app.config['IMGUR_CLIENT_SECRET'],
        current_app.config['IMGUR_ACCESS_TOKEN'],
        current_app.config['IMGUR_REFRESH_TOKEN']
    )

    post = Post()
    post.title = title
    post.description = description
    if User.query.filter(User.id.ilike(user_id)).first() is None:
        return jsonify(error="User inexistant"),404
    post.user_id = user_id

    # TODO : ajouter parallelisme
    image = imgur_client.upload_from_base64(image, config=config, anon=False)

    # on ajoute en DB l'url retourné par imgur
    post.url = image['link']

    db.session.add(post)
    db.session.commit()
    return post_schema.jsonify(post),200



    # datas = request.get_json()

    # description = datas.get('description', '')
    # if description is '':
    #     return jsonify(error="description vide"),400

    # url = datas.get('url', '')
    # if url is '':
    #     return jsonify(error="url vide"),400

    # post = Post()
    # post.description = description
    # post.url = url
    # post.user_id = user_id

    # db.session.add(post)
    # db.session.commit()
    # return post_schema.jsonify(post),200

    ######### GETTER POST

@api.route('/posts/<int:post_id>', methods=['GET'])
def get_post(post_id):
    post = Post.query.get(post_id)

    if post is not None:
        return post_schema.jsonify(post),200
    return jsonify(error="post not found"),404




####### DELETE POST


@api.route('/posts/<int:post_id>', methods=['DELETE'])
@authorized
def delete_post(user_id, post_id):
    # comme y'a le décorateur authorized, la fonction "delete_post"
    # connait le paramètre 'user_id'
    post = Post.query.get(post_id)
    if post is not None:
        if post.user_id == user_id:
            db.session.delete(post)
            db.session.commit()
            return jsonify(state=True),200
        return jsonify(error="This user can't delete this post!"),401
    return jsonify(error="post not found"),404

    ########### UPVOTE POST

@api.route('/posts/<int:post_id>/upvotes', methods=['POST'])
@authorized
def upvote_post(user_id, post_id):
    user = User.query.get(user_id)
    if user is not None:
        post = Post.query.get(post_id)
        if post is not None:
            #Checker que le post est pas déja dedans
            if post not in user.upvoted_posts:
                user.upvoted_posts.append(post)
                db.session.commit()
                return jsonify(state="ok"),200
            return jsonify(error="Post already upvoted by user"), 403
        return jsonify(error="post not found"),404
    return jsonify(error="user not found"),404


