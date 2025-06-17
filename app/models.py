from datetime import datetime
from app import db, login_manager
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True, nullable=False)
    email = db.Column(db.String(120), index=True, unique=True, nullable=False)
    password_hash = db.Column(db.String(256))
    locations = db.relationship('Location', backref='owner', lazy='dynamic')
    food_items = db.relationship('FoodItem', backref='owner', lazy='dynamic')

    def set_password(self, password):
        # from app import bcrypt
        # self.password_hash = bcrypt.generate_password_hash(password).decode('utf-8')
        pass
    
    def check_password(self, password):
        # from app import bcrypt
        # return bcrypt.check_password_hash(self.password_hash, password)
        pass

    def __repr__(self):
        return f'<User {self.username}>'
    
class Location(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    food_items = db.relationship('FoodItem', backref='location_assigned', lazy='dynamic', cascade="all, delete-orphan")

    def __repr__(self):
        return f'<FoodItem {self.name}>'
    
class FoodItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    quantity = db.Column(db.String(50), nullable=True) # Ex: "1 unidade", "500g"
    expiry_date = db.Column(db.Date, nullable=False)
    photo_filename = db.Column(db.String(100), nullable=True)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    
    # Chaves estrangeiras que ligam o item ao usuário e ao local
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    location_id = db.Column(db.Integer, db.ForeignKey('location.id'), nullable=True)

    def __repr__(self):
        return f'<FoodItem {self.name}>'