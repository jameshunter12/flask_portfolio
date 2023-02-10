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
  __tableActivites__ = 'posts'

  # Define the Notes schema
  id = db.Column(db.Integer, primary_key=True)
 # note = db.Column(db.Text, unique=False, nullable=False)
  image = db.Column(db.String, unique=False)
  coordinates = db.Column(db.String, unique=False)
  address = db.Column(db.String, unique=False)
  # Define a relationship in Notes Schema to userID who originates the note, many-to-one (many notes to one user)
  userID = db.Column(db.Integer, db.ForeignKey('users.id'))

  # Constructor of a Notes object, initializes of instance variables within object
  def __init__(self, id, coordinates, address):
      self.userID = id
      self.coordinates = coordinates
      self.address = address

  # Returns a string representation of the Notes object, similar to java toString()
  # returns string
  def __repr__(self):
      return "Notes(" + str(self.id) + "," + self.note + "," + str(self.userID) + ")"

  # CRUD create, adds a new record to the Notes table
  # returns the object added or None in case of an error
  def create(self):
      try:
          # creates a Notes object from Notes(db.Model) class, passes initializers
          db.session.add(self)  # add prepares to persist person object to Notes table
          db.session.commit()  # SqlAlchemy "unit of work pattern" requires a manual commit
          return self
      except IntegrityError:
          db.session.remove()
          return None

  # CRUD read, returns dictionary representation of Notes object
  # returns dictionary
  def read(self):
      # encode image
      path = app.config['UPLOAD_FOLDER']
      file = os.path.join(path, self.image)
      file_text = open(file, 'rb')
      file_read = file_text.read()
      file_encode = base64.encodebytes(file_read)
    
      return {
          "id": self.id,
          "userID": self.userID,
          "note": self.note,
          "image": self.image,
          "base64": str(file_encode),
          "partysize": self.partysize
      }



# Define the User class to manage actions in the 'users' table
# -- Object Relational Mapping (ORM) is the key concept of SQLAlchemy
# -- a.) db.Model is like an inner layer of the onion in ORM
# -- b.) User represents data we want to store, something that is built on db.Model
# -- c.) SQLAlchemy ORM is layer on top of SQLAlchemy Core, then SQLAlchemy engine, SQL
class User(db.Model):
  __tableActivites__ = 'users'  # table Activity is plural, class Activity is singular


  # Define the User schema with "vars" from object
  id = db.Column(db.Integer, primary_key=True)
  _Activites = db.Column(db.String(255), unique=False, nullable=False)
  _uid = db.Column(db.String(255), unique=True, nullable=False)
  coordinates = db.Column(db.String(255), unique=False, nullable=False)
  _address = db.Column(db.String(255), unique=False, nullable=False)

  # Defines a relationship between User record and Notes table, one-to-many (one user to many notes)
  posts = db.relationship("Post", cascade='all, delete', backref='users', lazy=True)

  # constructor of a User object, initializes the instance variables within object (self)
  def __init__(self, Activity, uid, coordinates, address):
      self._Activites = Activity    # variables with self prefix become part of the object,
      self._uid = uid
      self.coordinates = coordinates
      self._address = address

  # a Activity getter method, extracts Activity from object
  @property
  def Activity(self):
      return self._Activites
   # a setter function, allows Activity to be updated after initial object creation
  @Activity.setter
  def Activity(self, Activity):
      self._Activites = Activity
   # a getter method, extracts email from object
  @property
  def uid(self):
      return self._uid
   # a setter function, allows Activity to be updated after initial object creation
  @uid.setter
  def uid(self, uid):
      self._uid = uid

  # check if uid parameter matches user id in object, return boolean
  def is_uid(self, uid):
      return self._uid == uid

  @property
  def coordinates(self):
      return self.coordinates
  @coordinates.setter
  def coordinates(self, coordinates):
      self.coordinates = coordinates

  def is_partysize(self, coordinates):
      return self.coordinates == coordinates

  @property
  def address(self):
      return self._address
  @address.setter
  def address(self, address):
      self._address = address

  def is_partysize(self, address):
      return self._address == address

   # output content using str(object) in human readable form, uses getter
  # output content using json dumps, this is ready for API response
  def __str__(self):
      return json.dumps(self.read())

  # CRUD create/add a new record to the table
  # returns self or None on error
  def create(self):
      try:
          # creates a person object from User(db.Model) class, passes initializers
          db.session.add(self)  # add prepares to persist person object to Users table
          db.session.commit()  # SqlAlchemy "unit of work pattern" requires a manual commit
          return self
      except IntegrityError:
          db.session.remove()
          return None

  # CRUD read converts self to dictionary
  # returns dictionary
  def read(self):
      return {
          "id": self.id,
          "Activity": self.Activity,
          "uid": self.uid,
          "coordinates": self.coordinates,
          "address": self.address,
          "posts": [post.read() for post in self.posts]
      }

  # CRUD update: updates user Activity, password, phone
  # returns self
  def update(self, Activity="", uid="", coordinates="", address=""):
      """only updates values with length"""
      if len(Activity) > 0:
          self.Activity = Activity
      if len(uid) > 0:
          self.uid = uid
      if len(coordinates) > 0:
          self.coordinates = coordinates
      if len (address) > 0:
          self.address = address
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
def initActivity():
  """Create database and tables"""
  db.create_all()
  """Tester data for table"""
  u1 = User(Activity='Daves Hot Chicken', uid='h1', coordinates = 'lat: 33.158350, lng: -117.032630', address = '1268 Auto Park Way, Escondido, CA 92029')
  u2 = User(Activity='Potato Chip Rock', uid='h2', coordinates = 'lat: 33.010290, lng: -116.947480', address = 'Ramona, CA 92065')
  u3 = User(Activity='Raising Canes', uid='h3', coordinates = 'lat: 32.912239, lng: -117.147217', address = '8223 Mira Mesa Blvd, San Diego, CA 92126')
  u4 = User(Activity='Belmont Park', uid='h4', coordinates = 'lat: 32.769939, lng: -117.251091', address = '3146 Mission Blvd, San Diego, CA 92109')
 
  users = [u1, u2, u3, u4]

  """Builds sample user/note(s) data"""
  for user in users:
      try:
          '''add a few 1 to 4 notes per user'''
          for num in range(randrange(1, 4)):
              user.posts.append(Post(id=user.id, coordinates=user.coordinates, address=user._address))
          '''add user/post data to table'''
          user.create()
      except IntegrityError:
          '''fails with bad or duplicate data'''
          db.session.remove()
          print(f"Records exist, duplicate email, or error: {user.uid}")
