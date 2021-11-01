import marshmallow as ma


class User(ma.Schema):
    id = ma.fields.String()
    name = ma.fields.String(required=True, unique=True)
    email = ma.fields.Email(required=True, unique=True)
    created = ma.fields.DateTime()
    active = ma.fields.Boolean()
    salt = ma.fields.String()
    key = ma.fields.String()
    

class Group(ma.Schema):
    id = ma.fields.String()
    name = ma.fields.String(required=True, unique=True)
    users = ma.fields.Nested('User', many=True)
    created = ma.fields.DateTime()
    active = ma.fields.Boolean()


class Resource(ma.Schema):
    id = ma.fields.String()
    name = ma.fields.String(required=True, unique=True)
    owner = ma.fields.Nested('User')
    permissions = ma.fields.Nested('Permission', many=True)
    created = ma.fields.DateTime()
    active = ma.fields.Boolean()


class Permission(ma.Schema):
    id = ma.fields.String()
    resource = ma.fields.Nested('Resource')
    group = ma.fields.Nested('Group')
    user = ma.fields.Nested('User')
    created = ma.fields.DateTime()
    active = ma.fields.Boolean()
    update = ma.fields.Boolean()
    delete = ma.fields.Boolean()
    read = ma.fields.Boolean()