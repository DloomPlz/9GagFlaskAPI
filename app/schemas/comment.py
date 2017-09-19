from marshmallow import fields
from .. import ma

from ..models.comment import Comment

class CommentSchema(ma.ModelSchema):

    class Meta:
        model = Comment


comment_schema = CommentSchema()
comments_schema = CommentSchema(many=True)