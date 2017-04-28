from . import db

class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key = True)
    email = db.Column(db.String(20), unique = True)
    password = db.Column(db.String(10))
    name = db.Column(db.String(40))
    age = db.Column(db.String(3))
    gender = db.Column(db.String(6))
    image = db.Column(db.String(100))
    wishlist = db.relationship('Wishlist', backref = 'user', uselist = False)
    
    def __init__(self, email, password, name, age, gender, image):
        self.email = email
        self.password = password
        self.name = name
        self.age = age
        self.gender = gender
        self.image = image
        
    def is_authenticated(self):
        return True
    
    def is_active(self):
        return True
    
    def is_anonymous(self):
        return False
    
    def get_id(self):
        return self.id
        
    def __repr__(self):
        return '<User %r>' % (self.email)
        
class Wishlist(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    userid = db.Column(db.Integer, db.ForeignKey('user.id'))
    items = db.relationship('Items', backref='Wishlist', lazy='dynamic')
    
    def get_id(self):
        return self.id
            
class Items(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50))
    description = db.Column(db.String(255))
    url = db.Column(db.String(255))
    thumb = db.Column(db.String(255))
    price = db.Column(db.Float)
    wishlistId = db.Column(db.Integer, db.ForeignKey('Wishlist.id'))
    
    def get_id(self):
        return self.id