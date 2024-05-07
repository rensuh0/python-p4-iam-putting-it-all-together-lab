from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy_serializer import SerializerMixin
from sqlalchemy.orm import relationship

from config import db, bcrypt

class User(db.Model, SerializerMixin):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String)
    _password_hash= db.Column(db.String, nullable=False)
    image_url = db.Column(db.String)
    bio = db.Column(db.String)
    recipies = relationship('Recipie', backref='author', lazy=True)

    @hybrid_property
    def password_hash(self):
        return self._password_hash
    
    @password_hash.setter
    def password_hash(self, password):
        password_hash = bcrypt.generate_password_hash(
            password.encode('utf-8'))
        self._password_hash = password_hash.decode('utf-8')
    
    def authenticate(self, password):
        return bcrypt.check_password_hash(
            self._password_hash, password.encode('utf-8')
        )

class Recipe(db.Model, SerializerMixin):
    __tablename__ = 'recipes'
    
    id= db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    instructions= db.Column(db.String(50))
    minutes_to_complete = db.Column(db.Integer)
    user = db.relationship('User', backref=db.backref('recipies', lazy =True))
    
    