import sqlalchemy as sa
from sqlalchemy.orm import registry


mapper_registry = registry()


user = sa.Table(
    'user',
    mapper_registry.metadata,
    sa.Column('id', sa.String(24), primary_key=True),
    sa.Column('name', sa.String(64)),
    sa.Column('email', sa.String(128)),
    sa.Column('created', sa.DateTime),
    sa.Column('active', sa.Boolean),
    sa.Column('salt', sa.String(29)),
    sa.Column('key', sa.String(44)),
)


group = sa.Table(
    'group',
    mapper_registry.metadata,
    sa.Column('id', sa.String(24), primary_key=True),
    sa.Column('name', sa.String(64)),
    sa.Column('created', sa.DateTime),
    sa.Column('active', sa.Boolean),
    sa.Column('users', sa.ForeignKey('user.id'), many=True),
)


resource = sa.Table(
    'resource',
    mapper_registry.metadata,
    sa.Column('id', sa.String(24), primary_key=True),
    sa.Column('name', sa.String(64)),
    sa.Column('owner', sa.ForeignKey('user.id')),
    sa.Column('permissions', sa.ForeignKey('permission.id'), many=True),
    sa.Column('created', sa.DateTime),
    sa.Column('active', sa.Boolean),
)


permission = sa.Table(
    'permission',
    mapper_registry.metadata,
    sa.Column('id', sa.String(24), primary_key=True),
    sa.Column('resource', sa.ForeignKey('resource.id')),
    sa.Column('group', sa.ForeignKey('group.id')),
    sa.Column('user', sa.ForeignKey('user.id')),
    sa.Column('created', sa.DateTime),
    sa.Column('active', sa.Boolean),
    sa.Column('update', sa.Boolean),
    sa.Column('delete', sa.Boolean),
    sa.Column('read', sa.Boolean),
)