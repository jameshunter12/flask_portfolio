""" database dependencies to support sqliteDB examples """
from random import randrange
from datetime import date
import os, base64
import json

from __init__ import app, db
from sqlalchemy.exc import IntegrityError
from werkzeug.security import generate_password_hash, check_password_hash


''' Tutorial: https://www.sqlalchemy.org/library.html#tutorials, try to get into Python shell and follow along '''

# Define the Post class to manage actions in 'posts' table,  with a relationship to 'users' table
class Post(db.Model):
    __tablename__ = 'posts'

    # Define the classofs schema
    id = db.Column(db.Integer, primary_key=True)
    classof = db.Column(db.Text, unique=False, nullable=False)
    dob = db.Column(db.String, unique=False)
    # Define a relationship in classofs Schema to userID who originates the classof, many-to-one (many classofs to one user)
    userID = db.Column(db.Integer, db.ForeignKey('users.id'))

    # Constructor of a classofs object, initializes of instance variables within object
    def __init__(self, id, classof, dob):
        self.userID = id
        self.classof = classof
        self.dob = dob

    # Returns a string representation of the classofs object, similar to java toString()
    # returns string
    def __repr__(self):
        return "classofs(" + str(self.id) + "," + self.classof + "," + str(self.userID) + ")"

    # CRUD create, adds a new record to the classofs table
    # returns the object added or None in case of an error
    def create(self):
        try:
            # creates a classofs object from classofs(db.Model) class, passes initializers
            db.session.add(self)  # add prepares to persist person object to classofs table
            db.session.commit()  # SqlAlchemy "unit of work pattern" requires a manual commit
            return self
        except IntegrityError:
            db.session.remove()
            return None

    # CRUD read, returns dictionary representation of classofs object
    # returns dictionary
    def read(self):
        # encode dob
        path = app.config['UPLOAD_FOLDER']
        file = os.path.join(path, self.dob)
        file_text = open(file, 'rb')
        file_read = file_text.read()
        file_encode = base64.encodebytes(file_read)
        
        return {
            "id": self.id,
            "userID": self.userID,
            "classof": self.classof,
            "dob": self.dob,
            "age": self.age
        }


# Define the User class to manage actions in the 'users' table
# -- Object Relational Mapping (ORM) is the key concept of SQLAlchemy
# -- a.) db.Model is like an inner layer of the onion in ORM
# -- b.) User represents data we want to store, something that is built on db.Model
# -- c.) SQLAlchemy ORM is layer on top of SQLAlchemy Core, then SQLAlchemy engine, SQL
class User(db.Model):
    __tablename__ = 'users'  # table name is plural, class name is singular

    # Define the User schema with "vars" from object
    id = db.Column(db.Integer, primary_key=True)
    _name = db.Column(db.String(255), unique=False, nullable=False)
    _uid = db.Column(db.String(255), unique=True, nullable=False)
    _password = db.Column(db.String(255), unique=False, nullable=False)
    _dob = db.Column(db.Date)

    # Defines a relationship between User record and classofs table, one-to-many (one user to many classofs)
    posts = db.relationship("Post", cascade='all, delete', backref='users', lazy=True)

class User:    

    def __init__(self, name, uid, classof, password, dob):
        self._name = name    # variables with self prefix become part of the object, 
        self._uid = uid
        self._classof = classof
        self.set_password(password)
        self._dob = dob
    
    @property
    def name(self):
        return self._name
    
    # a setter function, allows name to be updated after initial object creation
    @name.setter
    def name(self, name):
        self._name = name
    
    # a getter method, extracts email from object
    @property
    def uid(self):
        return self._uid
    
    # a setter function, allows name to be updated after initial object creation
    @uid.setter
    def uid(self, uid):
        self._uid = uid
        
    # check if uid parameter matches user id in object, return boolean
    def is_uid(self, uid):
        return self._uid == uid
    
    @property
    def classof(self):
        return self._classof
    
    @classof.setter
    def classof(self, classof):
        self.classof = classof
    
    # dob property is returned as string, to avoid unfriendly outcomes
    @property
    def dob(self):
        dob_string = self._dob.strftime('%m-%d-%Y')
        return dob_string
    
    # dob should be have verification for type date
    @dob.setter
    def dob(self, dob):
        self._dob = dob
        
    # age is calculated and returned each time it is accessed
    @property
    def age(self):
        today = date.today()
        return today.year - self._dob.year - ((today.month, today.day) < (self._dob.month, self._dob.day))
    
    # dictionary is customized, removing password for security purposes
    @property
    def dictionary(self):
        dict = {
            "name" : self.name,
            "uid" : self.uid,
            "classof" : self.classof,
            "dob" : self.dob,
            "age" : self.age
        }
# CRUD update: updates user name, password, phone
    # returns self
    def update(self, name="", uid="", password=""):
        """only updates values with length"""
        if len(name) > 0:
            self.name = name
        if len(uid) > 0:
            self.uid = uid
        if len(password) > 0:
            self.set_password(password)
        db.session.commit()
        return self

    # CRUD delete: remove self
    # None
    def delete(self):
        db.session.delete(self)
        db.session.commit()
        return None

"""Database Creation and Testing """


# Builds working data for testing
def initUsers():
    """Create database and tables"""
    db.create_all()
    """Tester data for table"""
    u1 = User(name='Thomas Edison', uid='toby', password='123toby', dob=date(1847, 2, 11))
    u2 = User(name='Nicholas Tesla', uid='niko', password='123niko')
    u3 = User(name='Alexander Graham Bell', uid='lex', password='123lex')
    u4 = User(name='Eli Whitney', uid='whit', password='123whit')
    u5 = User(name='John Mortensen', uid='jm1021', dob=date(1959, 10, 21))

    users = [u1, u2, u3, u4, u5]

    """Builds sample user/classof(s) data"""
    for user in users:
        try:
            '''add a few 1 to 4 classofs per user'''
            for num in range(randrange(1, 4)):
                classof = "#### " + user.name + " classof " + str(num) + ". \n Generated by test data."
                user.posts.append(Post(id=user.id, classof=classof, dob='ncs_logo.png'))
            '''add user/post data to table'''
            user.create()
        except IntegrityError:
            '''fails with bad or duplicate data'''
            db.session.remove()
            print(f"Records exist, duplicate email, or error: {user.uid}")
            