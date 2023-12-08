from bestsellers import app, db
from flask_sqlalchemy import SQLAlchemy
from flask_user import UserMixin

def tablename(t):
    tname = app.config.get('TABLE_PREFIX')
    if tname is not None and len(tname) > 0:
        return tname+"_"+t
    else:
        return t

class User(db.Model, UserMixin):
    __tablename__ = tablename('user')

    id = db.Column(db.Integer, primary_key=True)

    username = db.Column(db.String(50), nullable=False, unique=True)
    password = db.Column(db.String(255), nullable=False, server_default='')
    reset_password_token = db.Column(db.String(100), nullable=False, server_default='')

    email = db.Column(db.String(255), nullable=False, unique=True)
    confirmed_at = db.Column(db.DateTime())

    active = db.Column('is_active', db.Boolean(), nullable=False, server_default='0')
    first_name = db.Column(db.String(100), nullable=False, server_default='')
    last_name = db.Column(db.String(100), nullable=False, server_default='')
    
    anonymous = db.Column(db.Boolean(), nullable=False, server_default='0')

    # Define relationships for user
    book = db.relationship('Book', uselist=False, backref='user', lazy='joined')
    answers = db.relationship('Answers', backref='user', lazy='joined')
    supplements = db.relationship('Supplement', backref='user', lazy='joined')
    roles = db.relationship('Role', secondary='user_roles',
                            backref=db.backref('users', lazy='dynamic'))
    
    @property
    def name(self):
        if self.anonymous:
            return 'Anonymous, by request'
        elif self.last_name:
            return self.first_name+' '+self.last_name
        else:
            return self.username
            
    @property
    def admin_name(self):
        if self.last_name:
            return self.first_name+' '+self.last_name
        else:
            return self.username
            
    
class Role(db.Model):
    __tablename__ = tablename('role')
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(50), unique=True)

class UserRoles(db.Model):
    __tablename__ = tablename('user_roles')
    id = db.Column(db.Integer(), primary_key=True)
    user_id = db.Column(db.Integer(), db.ForeignKey('user.id', ondelete='CASCADE'))
    role_id = db.Column(db.Integer(), db.ForeignKey('role.id', ondelete='CASCADE'))

class Book(db.Model):
    __tablename__ = tablename('books')
    id = db.Column(db.Integer(), primary_key=True)
    type = db.Column(db.String(2), nullable=False, server_default='F')
    taken_by = db.Column(db.Integer(), db.ForeignKey('user.id'))
    title = db.Column(db.String(255), nullable=False, server_default='')
    author = db.Column(db.String(255), nullable=False, server_default='')
    years = db.relationship('YearList', backref='book', lazy='joined')

class YearList(db.Model):
    __tablename__ = tablename('years')
    id = db.Column(db.Integer(), primary_key=True)
    book_id = db.Column('bsid', db.Integer(), db.ForeignKey(Book.id))
    year = db.Column(db.Integer())
    rank = db.Column(db.Integer())
    tie = db.Column(db.Boolean())

class Assignments(db.Model):
    __tablename__ = tablename('assignments')
    id = db.Column(db.Integer(), primary_key=True)
    order = db.Column(db.Integer())
    name = db.Column(db.String(300))
    #text = db.Column(db.Text()) #moved this into templates/help/a#short.html
    questions = db.relationship('Questions', backref='assignment', lazy='joined')

class Questions(db.Model):
    __tablename__ = tablename('questions')
    id = db.Column(db.Integer(), primary_key=True)
    assignment_id = db.Column(db.Integer(), db.ForeignKey(Assignments.id))
    order = db.Column(db.Integer())
    text = db.Column(db.Text())
    type = db.Column(db.Enum('image','text'))
    answers = db.relationship('Answers', backref='question', lazy='joined')

class Answers(db.Model):
    __tablename__ = tablename('answers')
    id = db.Column(db.Integer(), primary_key=True)
    question_id = db.Column(db.Integer(), db.ForeignKey(Questions.id))
    user_id = db.Column(db.Integer(), db.ForeignKey(User.id))
    text = db.Column(db.Text())

class Supplement(db.Model):
    __tablename__ = tablename('supplements')
    id = db.Column(db.Integer(), primary_key=True)
    user_id = db.Column(db.Integer(), db.ForeignKey(User.id))
    order = db.Column('display_order', db.Integer())
    description = db.Column(db.Text())
    type = db.Column(db.Enum('image','text'))
    data = db.Column(db.Text())
    
class Setting(db.Model):
    __tablename__ = tablename('admin_config')
    name = db.Column(db.Text(), primary_key=True)
    value = db.Column(db.Text())
