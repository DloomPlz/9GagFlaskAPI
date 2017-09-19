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

########## CREATE POST
@api.route('/posts', methods=['POST'])
@authorized
def create_post(user_id):
    # datas = request.get_json()
    # image=datas.get('image','')
    #     if image is not '':
    #     #changer la config par les valeurs du JSON, laisser None dans album
    #     config = {
    #         'album': None,
    #         'name':  'Catastrophe!',
    #         'title': 'Catastrophe!',
    #         'description': 'Cute kitten being dead'
    #     }
    #     #penser à import current_app
    #     # imgur_client = ImgurClient(
    #     #     current_app.config['IMGUR_CLIENT_ID'],
    #     #     current_app.config['IMGUR_CLIENT_SECRET'],
    #     #     current_app.config['IMGUR_ACCESS_TOKEN'],
    #     #     current_app.config['IMGUR_REFRESH_TOKEN']
    #     # )
    #     imgur_client = ImgurClient(
    #         '891edbe392e448f',
    #         'ed66022b-ee9c-4047-9482-f1dff8addae1',
    #         '6de37753376a790d346d5095a5eb2ad331ce4e01',
    #         '224f62de0522d94a4f400396ebed374ff2199cd5'
    #     )
    #     image = imgur_client.upload_from_base64(image, config=config, anon=False)

    #     # on ajoute en DB l'url retourné par imgur
    #     # image.url = image['link']

    #     # tu remarqueras qu'ici l'upload peut être très long selon le poids de l'image
    #     # il va falloir songer à "paralleliser" les taches, car là tant que le fichier upload,
    #     # tout ton serveur est en attente -> pas cool
    #     # donc faudra songer à ajouter du parallelisme ici
    #     # LMGTFY : flask parallel ou python thread
    #     # TODO : ajouter parallelisme
    #     return jsonify(image=image['link']),200
    # return jsonify(error="image not in JSON"),400
    datas = request.get_json()

    description = datas.get('description', '')
    if description is '':
        return jsonify(error="description vide"),400

    url = datas.get('url', '')
    if url is '':
        return jsonify(error="url vide"),400

    post = Post()
    post.description = description
    post.url = url
    post.user_id = user_id

    db.session.add(post)
    db.session.commit()
    return post_schema.jsonify(post),200

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


