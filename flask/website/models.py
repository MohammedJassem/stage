from website import db,login_manager,app
from website import bcrypt
from flask_user import UserMixin
from flask_sqlalchemy import SQLAlchemy
from flask_user import UserManager,SQLAlchemyAdapter





@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model,UserMixin):


    id = db.Column(db.Integer(), primary_key=True)
    username = db.Column(db.String(length=30), nullable=False, unique=True)
    email_address = db.Column(db.String(length=50), nullable=False, unique=True)
    password_hash = db.Column(db.String(length=60), nullable=False)
    Admin_key = db.Column(db.String(length=10), nullable=True, unique=True)
    role_id = db.Column(db.Integer(), db.ForeignKey('role.id'), nullable=False) 

    @property
    def password(self):
        return self.password

    @password.setter
    def password(self, plain_text_password):
        self.password_hash = bcrypt.generate_password_hash(plain_text_password).decode('utf-8')

    def check_password_correction(self, attempted_password):
        return bcrypt.check_password_hash(self.password_hash, attempted_password)

class Admin(db.Model,UserMixin):
    __tablename__ = 'admin'
    id = db.Column(db.Integer(), primary_key=True)
    username = db.Column(db.String(length=30), nullable=False, unique=True)
    email_address = db.Column(db.String(length=50), nullable=False, unique=True)
    password_hash = db.Column(db.String(length=60), nullable=False)
    Admin_key = db.Column(db.String(length=10), nullable=False, unique=True)
    #roles = db.relationship('Role', secondary='user_roles')

    @property
    def password(self):
        return self.password

    @password.setter
    def password(self, plain_text_password):
        self.password_hash = bcrypt.generate_password_hash(plain_text_password).decode('utf-8')

    def check_password_correction(self, attempted_password):
        return bcrypt.check_password_hash(self.password_hash, attempted_password)

    
class Item(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    soil_moisture = db.Column(db.String(length=30), nullable=False, unique=False)
    status = db.Column(db.Integer(), nullable=False)
    time = db.Column(db.String(length=12), nullable=False, unique=False)
    sensor_location = db.Column(db.String(length=1024), nullable=False, unique=False)

    def __repr__(self):
        return 'Item {}'.format(self.name)


class Role(db.Model):
  
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(50), unique=False)
    users = db.relationship('User', backref='role', lazy=True, primaryjoin="Role.id == User.role_id")



db_adapter = SQLAlchemyAdapter(db,User)
user_manager = UserManager(db_adapter,app)

