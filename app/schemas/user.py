from marshmallow import fields
from .. import ma
from ..models.user import User

class UserSchema(ma.ModelSchema):

	id = fields.Int()
	username = fields.String()
	email = fields.String()

user_schema = UserSchema()
users_schema = UserSchema(many=True)