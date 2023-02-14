""" database dependencies to support sqliteDB examples """
from random import randrange
from datetime import date
import os, base64
import json
from __init__ import app, db
from sqlalchemy.exc import IntegrityError
from werkzeug.security import generate_password_hash, check_password_hash


''' Tutorial: https://www.sqlalchemy.org/library.html#tutorials, try to get into Python shell and follow along '''


# Define the Post class to manage actions in 'Posts' table,  with a relationship to 'activitys' table
class Post(db.Model):
  __tablename__ = 'Posts'

  # Define the Notes schema
  id = db.Column(db.Integer, primary_key=True)
 # note = db.Column(db.Text, unique=False, nullable=False)
  image = db.Column(db.String, unique=False)
  address = db.Column(db.String, unique=False)
  coordinates = db.Column(db.String, unique=False)
  fun = db.Column(db.String, unique=False)
  # Define a relationship in Notes Schema to activityID who originates the note, many-to-one (many notes to one activity)
  activityID = db.Column(db.Integer, db.ForeignKey('activitys.id'))

  # Constructor of a Notes object, initializes of instance variables within object
  def __init__(self, id, address, coordinates, fun):
      self.activityID = id
      self.address = address
      self.coordinates = coordinates
      self.fun = fun

  # Returns a string representation of the Notes object, similar to java toString()
  # returns string
  def __repr__(self):
      return "Notes(" + str(self.id) + "," + self.note + "," + str(self.activityID) + ")"

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
          "activityID": self.activityID,
          "note": self.note,
          "image": self.image,
          "base64": str(file_encode),
          "partysize": self.partysize
      }

# Define the activity class to manage actions in the 'activitys' table
# -- Object Relational Postping (ORM) is the key concept of SQLAlchemy
# -- a.) db.Model is like an inner layer of the onion in ORM
# -- b.) activity represents data we want to store, something that is built on db.Model
# -- c.) SQLAlchemy ORM is layer on top of SQLAlchemy Core, then SQLAlchemy engine, SQL
class activity(db.Model):
  __tablename__ = 'activities'  # table name is plural, class name is singular

  # Define the activity schema with "vars" from object
  id = db.Column(db.Integer, primary_key=True)
  _name = db.Column(db.String(255), unique=False, nullable=False)
  _uid = db.Column(db.String(255), unique=True, nullable=False)
  _fun = db.Column(db.String(255), unique=False, nullable=True)
  _address = db.Column(db.String(255), unique=False, nullable=False)
  _coordinates = db.Column(db.String(255), unique=False, nullable=False)

  # Defines a relationship between activity record and Notes table, one-to-many (one activity to many notes)
  Posts = db.relationship("Post", cascade='all, delete', backref='activitys', lazy=True)

  # constructor of a activity object, initializes the instance variables within object (self)
  def __init__(self, name, uid, address, coordinates ,fun):
      self._name = name    # variables with self prefix become part of the object,
      self._uid = uid
      self._address = address
      self._coordinates = coordinates
      self._fun = fun

  # a name getter method, extracts name from object
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

  # check if uid parameter matches activity id in object, return boolean
  def is_uid(self, uid):
      return self._uid == uid

  @property
  def address(self):
      return self._address
  @address.setter
  def address(self, address):
      self._address = address

  def is_partysize(self, address):
      return self._address == address

  @property
  def coordinates(self):
      return self._coordinates
  @coordinates.setter
  def coordinates(self, coordinates):
      self._coordinates = coordinates

  def is_partysize(self, coordinates):
      return self._coordinates == coordinates
 
  @property
  def fun(self):
      return self._fun
  @fun.setter
  def fun(self, fun):
      self._fun = fun

  def is_partysize(self, fun):
      return self._fun == fun
   # output content using str(object) in human readable form, uses getter
  # output content using json dumps, this is ready for API response
  def __str__(self):
      return json.dumps(self.read())

  # CRUD create/add a new record to the table
  # returns self or None on error
  def create(self):
      try:
          # creates a person object from activity(db.Model) class, passes initializers
          db.session.add(self)  # add prepares to persist person object to activitys table
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
          "name": self.name,
          "uid": self.uid,
          "address": self.address,
          "coordinates": self.coordinates,
          "fun": self.fun,
          "Posts": [Post.read() for Post in self.Posts]
      }

  # CRUD update: updates activity name, password, phone
  # returns self
  def update(self, name="", uid="", address="", coordinates="", fun=""):
      """only updates values with length"""
      if len(name) > 0:
          self.name = name
      if len(uid) > 0:
          self.uid = uid
      if len(address) > 0:
          self.address = address
      if len (coordinates) > 0:
          self.coordinates = coordinates
      if len(fun) > 0:
          self.fun = fun   
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
  a1 = activity(name='Daves Hot Chicken', uid='h1', address = '1268 Auto Park Way, Escondido, CA 92029', coordinates = 'lat: 33.158350, lng: -117.032630', fun='8/10')
  a2 = activity(name='Raising Canes', uid='h2', address = '8223 Mira Mesa Blvd, San Diego, CA 92126', coordinates = 'lat: 32.912239, lng: -117.147217', fun='10/10')
  a3 = activity(name='Belmont Park', uid='h3', address = '3146 Mission Blvd, San Diego, CA 92109', coordinates = 'lat: 32.769939, lng: -117.251091', fun='7/10')
  a4 = activity(name='Potato Chip Rock', uid='h4', address = 'Ramona, CA 92065', coordinates = 'lat: 33.010290, lng: -116.947480', fun='6/10')

  activities = [a1, a2, a3, a4]

  """Builds sample activity/note(s) data"""
  for activity in activities:
      try:
          '''add a few 1 to 4 notes per activity'''
          for num in range(randrange(1, 4)):
              activity.Posts.append(Post(id=activity.id, address=activity._address, coordinates=activity._coordinates ,fun = activity._fun))
          '''add activity/Post data to table'''
          activity.create()
      except IntegrityError:
          '''fails with bad or duplicate data'''
          db.session.remove()
          print(f"Records exist, duplicate email, or error: {activity.uid}")


