from flask_sqlalchemy import SQLAlchemy
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
        '''REturn full name'''
        return f'{self.first_name} {self.last_name}'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    image_url = db.Column(db.Text, default=DEFAULT_IMAGE_URL )