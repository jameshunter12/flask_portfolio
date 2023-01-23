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

  # Define the Notes schema
  id = db.Column(db.Integer, primary_key=True)
  note = db.Column(db.Text, unique=False, nullable=False)
  image = db.Column(db.String, unique=False)
  duroftrip = db.Column(db.String, unique=False)
  # Define a relationship in Notes Schema to userID who originates the note, many-to-one (many notes to one user)
  userID = db.Column(db.Integer, db.ForeignKey('users.id'))


  # Constructor of a Notes object, initializes of instance variables within object
  def __init__(self, id, note, image, duroftrip):
      self.userID = id
      self.note = note
      self.image = image
      self.duroftrip = duroftrip


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
          "duroftrip": self.duroftrip
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
  _duroftrip = db.Column(db.String(255), unique=False, nullable=False)
  _password = db.Column(db.String(255), unique=False, nullable=False)
  _dob = db.Column(db.Date)




  # Defines a relationship between User record and Notes table, one-to-many (one user to many notes)
  posts = db.relationship("Post", cascade='all, delete', backref='users', lazy=True)




  # constructor of a User object, initializes the instance variables within object (self)
  def __init__(self, name, uid, duroftrip,  password="123qwerty", dob=date.today(),):
      self._name = name    # variables with self prefix become part of the object,
      self._uid = uid
      self.duroftrip = duroftrip
      self.set_password(password)
      self._dob = dob




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


  # check if uid parameter matches user id in object, return boolean
  def is_uid(self, uid):
      return self._uid == uid


  @property
  def duroftrip(self):
      return self._duroftrip
  @duroftrip.setter
  def duroftrip(self, duroftrip):
      self._duroftrip = duroftrip

  def is_duroftrip(self, duroftrip):
      return self._duroftrip == duroftrip

  @property
  def password(self):
      return self._password[0:10] + "..." # because of security only show 1st characters

  # update password, this is conventional setter
  def set_password(self, password):
      """Create a hashed password."""
      self._password = generate_password_hash(password, method='sha256')


  # check password parameter versus stored/encrypted password
  def is_password(self, password):
      """Check against hashed password."""
      result = check_password_hash(self._password, password)
      return result
   # dob property is returned as string, to avoid unfriendly outcomes
  @property
  def dob(self):
      dob_string = self._dob.strftime('%m-%d-%Y')
      return dob_string
   # dob should be have verification for type date
  @dob.setter
  def dob(self, dob):
      self._dob = dob
  @property
  def age(self):
      today = date.today()
      return today.year - self._dob.year - ((today.month, today.day) < (self._dob.month, self._dob.day))
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
          "name": self.name,
          "uid": self.uid,
          "duroftrip": self.duroftrip,
          "dob": self.dob,
          "age": self.age,
          "posts": [post.read() for post in self.posts]
      }




  # CRUD update: updates user name, password, phone
  # returns self
  def update(self, name="", uid="", duroftrip="", password=""):
      """only updates values with length"""
      if len(name) > 0:
          self.name = name
      if len(uid) > 0:
          self.uid = uid
      if len(duroftrip) > 0:
          self.duroftrip = duroftrip
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
  u1 = User(name='Qais J', uid='qais', duroftrip='3 days', password='123qais', dob=date(2007, 2, 11))
  u2 = User(name='James H', uid='james', duroftrip='4 days', password='123james')
  u3 = User(name='Krishiv M', uid='krishiv', duroftrip='7 days', password='123krishiv')
  u4 = User(name='Caleb N', uid='caleb', duroftrip='6 days', password='123caleb')
  u5 = User(name='Mr Yeung', uid='yeung', duroftrip='1 day', dob=date(1990, 10, 21))
  u6 = User(name='Mr Mort', uid='mort', duroftrip='2 days', dob=date(1980, 10, 13))

  users = [u1, u2, u3, u4, u5, u6]







  """Builds sample user/note(s) data"""
  for user in users:
      try:
          '''add a few 1 to 4 notes per user'''
          for num in range(randrange(1, 4)):
              note = "#### " + user.name + " note " + str(num) + ". \n Generated by test data."
              user.posts.append(Post(id=user.id, note=note, duroftrip=note , image='ncs_logo.png',))
          '''add user/post data to table'''
          user.create()
      except IntegrityError:
          '''fails with bad or duplicate data'''
          db.session.remove()
          print(f"Records exist, duplicate email, or error: {user.uid}")
        

