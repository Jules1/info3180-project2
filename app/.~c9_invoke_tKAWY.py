from . import db

class User(db.Model):
    id = db.Column('user_id', db.Integer, primary_key = True)
    email = db.Column(db.String(20), unique = True)
    password = db.Column(db.String(10))
    name = db.Column(db.String(40))
    age = db.Column(db.Float)
    gender = db.Column(db.String(6))
    image = db.Column(db.String(100))
    
def __init__(self, email, password, name, age, gender, image):
    self.email = email
    self.password = password
    self.name = name
    self.age = age
    self.gender = gender
    self.image = image
    












