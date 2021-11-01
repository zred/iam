import datetime as dt
from uuid import uuid1
from bcrypt import gensalt,kdf
from base64 import urlsafe_b64encode
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session, registry
from iam.models import (
    user as UserModel,
    group as GroupModel,
    resource as ResourceModel,
    permission as PermissionModel,
)
from iam.schema import (
    User as UserSchema,
    Group as GroupSchema,
    Resource as ResourceSchema,
    Permission as PermissionSchema,
)


engine = create_engine('sqlite:///iam.db', echo=True)
session = scoped_session(sessionmaker(bind=engine))
mapper_registry = registry()


class User:
    def __init__(self, name, email):
        self.name = name
        self.email = email
        self.salt = gensalt()
        self.created = dt.datetime.now()
        self.id =  urlsafe_b64encode(uuid1().bytes)
        self.active = True
    
    def __repr__(self):
        return f"{UserSchema().dump(self)}"

    def set_password(self,password):
        self.key = urlsafe_b64encode(kdf(
            password=password,
            salt=self.salt,
            desired_key_bytes=32,
            rounds=100,
        ))

    def authenticate(self,password):
        return self.key == urlsafe_b64encode(kdf(
            password=password,
            salt=self.salt,
            desired_key_bytes=32,
            rounds=100
        ))

    def toggle_active(self):
        self.active = not self.active

    def save(self, session):
        session.add(self)
        session.commit()

    def delete(self, session):
        session.delete(self)
        session.commit()

    def update(self, session, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)
        session.commit()


mapper_registry.map_imperatively(User, UserModel)


class Group:
    def __init__(self, name):
        self.name = name
        self.created = dt.datetime.now()
        self.id =  urlsafe_b64encode(uuid1().bytes)
        self.active = True
        self.users = []
    
    def __repr__(self):
        return f"{GroupSchema().dump(self)}"

    def add_user(self,user):
        self.users.append(user)

    def remove_user(self,user):
        self.users.remove(user)

    def toggle_active(self):
        self.active = not self.active

    def save(self):
        session.add(self)
        session.commit()

    def delete(self):
        session.delete(self)
        session.commit()

    def update(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)
        session.commit()


mapper_registry.map_imperatively(Group, GroupModel)


class Resource:
    def __init__(self, name, owner):
        self.name = name
        self.owner = owner
        self.permissions = []
        self.created = dt.datetime.now()
        self.id =  urlsafe_b64encode(uuid1().bytes)
        self.active = True
    
    def __repr__(self):
        return f"{ResourceSchema().dump(self)}"

    def toggle_active(self):
        self.active = not self.active

    def add_permission(self,permission):
        self.permissions.append(permission)

    def save(self):
        session.add(self)
        session.commit()

    def delete(self):
        session.delete(self)
        session.commit()

    def update(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)
        session.commit()


mapper_registry.map_imperatively(Resource, ResourceModel)


class Permission:
    def __init__(self, resource, group, user):
        self.resource = resource
        self.group = group
        self.user = user
        self.created = dt.datetime.now()
        self.id =  urlsafe_b64encode(uuid1().bytes)
        self.active = True
        self.update = False
        self.delete = False
        self.read = False

    def __repr__(self):
        return f"{PermissionSchema().dump(self)}"

    def toggle_active(self):
        self.active = not self.active

    def save(self):
        session.add(self)
        session.commit()

    def delete(self):
        session.delete(self)
        session.commit()

    def update(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)
        session.commit()


mapper_registry.map_imperatively(Permission, PermissionModel)


UserModel.create_table(engine, checkfirst=True)
GroupModel.create_table(engine, checkfirst=True)
ResourceModel.create_table(engine, checkfirst=True)
PermissionModel.create_table(engine, checkfirst=True)