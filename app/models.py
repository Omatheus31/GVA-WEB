from datetime import datetime
from .extensions import db, login_manager, bcrypt
from flask_login import UserMixin
from flask import current_app
import jwt
import time

@login_manager.user_loader
def load_user(user_id):
    user = User.query.get(int(user_id))
    return user

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True, nullable=False)
    email = db.Column(db.String(120), index=True, unique=True, nullable=False)
    password_hash = db.Column(db.String(256))
    tfa_secret = db.Column(db.String(32), nullable=True)
    tfa_enabled = db.Column(db.Boolean, nullable=False, server_default='false')
    is_admin = db.Column(db.Boolean, nullable=False, server_default='false')

    locations = db.relationship('Location', backref='owner', lazy='dynamic', cascade="all, delete-orphan")
    food_items = db.relationship('FoodItem', backref='owner', lazy='dynamic', cascade="all, delete-orphan")
    audit_logs = db.relationship('AuditLog', backref='user_log', lazy='dynamic', cascade="all, delete-orphan")

    def set_password(self, password):
        self.password_hash = bcrypt.generate_password_hash(password).decode('utf-8')
        
    def check_password(self, password):
        return bcrypt.check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f'<User {self.username}>'
    
    def get_reset_password_token(self):
        """
        Gera um token JWT seguro que contém o ID do usuário e um tempo de expiração.
        O token é assinado com a SECRET_KEY da aplicação para garantir sua autenticidade.
        """
        expires_in = current_app.config['PASSWORD_RESET_TOKEN_EXPIRES']
        return jwt.encode(
            {'reset_password': self.id, 'exp': time.time() + expires_in},
            current_app.config['SECRET_KEY'],
            algorithm='HS256'
        )
    
    @staticmethod
    def verify_reset_password_token(token):
        try:
            id = jwt.decode(
                token,
                current_app.config['SECRET_KEY'],
                algorithms=['HS256']
            )['reset_password']
        except: 
            return None
        
        return User.query.get(id)
    
class Location(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    food_items = db.relationship('FoodItem', backref='location_assigned', lazy='dynamic', cascade="all, delete-orphan")

    def __repr__(self):
        return f'<Location {self.name}>'
    
class FoodItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    quantity = db.Column(db.String(50), nullable=True)
    expiry_date = db.Column(db.Date, nullable=False)
    photo_filename = db.Column(db.String(100), nullable=True)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    location_id = db.Column(db.Integer, db.ForeignKey('location.id'), nullable=True)

    def __repr__(self):
        return f'<FoodItem {self.name}>'
    
class AuditLog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)
    ip_address = db.Column(db.String(45))
    action = db.Column(db.String(256), nullable=False)
    details = db.Column(db.String(512), nullable=True)

    user = db.relationship('User', backref='user_log_entries')

    def __repr__(self):
        return f'<AuditLog {self.timestamp} - {self.action}>'