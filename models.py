from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
"""Models for Blogly."""

db = SQLAlchemy()
DEFAULT_IMAGE_URL = 'https://cdn.pixabay.com/photo/2015/10/05/22/37/blank-profile-picture-973460_960_720.png'

def connect_db(app):
    '''Connect to database.'''
    db.app = app
    db.init_app(app)

class User(db.Model):
    '''User.'''
    __tablename__='users'

    def __repr__(self):
        u = self
        return f'<User id={u.id}, first_name={u.first_name}, last_name={u.last_name}, image_url={u.image_url}>'
    
    @property
    def full_name(self):
        '''Return full name'''
        return f'{self.first_name} {self.last_name}'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    image_url = db.Column(db.Text, nullable=False, default=DEFAULT_IMAGE_URL )

class Post(db.Model):
    '''Post.'''
    __tablename__='posts'

    def __repr__(self):
        p = self
        return f'<Post id={p.id}, title={p.title}, content={p.content}, created_at={p.created_at}, user_id={p.user_id} >'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(50), nullable=False)
    content = db.Column(db.String(200), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.now())
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    user = db.relationship('User', backref='posts')
