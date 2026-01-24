from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash


db = SQLAlchemy()

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)


    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Equation(db.Model):
    id_equation = db.Column(db.Integer, primary_key=True)
    id_user = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    level = db.Column(db.String(10), nullable=False)
    type = db.Column(db.String(10), nullable=False)
    id_function = db.Column(db.Integer, db.ForeignKey('function.id'), nullable=True)

    equation = db.Column(db.String(100), nullable=False)
    roots = db.Column(db.String(50), nullable=False)
    steps = db.Column(db.Text, nullable=False)

    day_generated = db.Column(db.DateTime, nullable=False, default=datetime.now)


    
class Function(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    id_user = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    type = db.Column(db.String(10), nullable=False)
    id_equation = db.Column(db.Integer, db.ForeignKey('equation.id_equation'), nullable=True)

    val_a = db.Column(db.Integer, nullable=False)
    val_bn = db.Column(db.Integer, nullable=False)
    val_bd = db.Column(db.Integer, nullable=False)
    val_v = db.Column(db.Integer, nullable=True)
    val_n = db.Column(db.Integer, nullable=True)
    val_k = db.Column(db.Integer, nullable=True)
    val_px = db.Column(db.String(50), nullable=True)
    val_py = db.Column(db.String(50), nullable=True)
    # id_coefficients = db.Column(db.Integer, db.ForeignKey('function_coefficients.id_coefficients'), nullable=False)
    day_generated = db.Column(db.DateTime, nullable=False, default=datetime.now)
