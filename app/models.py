from .extensions import db
import sqlalchemy as models
from flask_login import UserMixin

class TestTable(db.Model):
    __tabelname__ = 'Tests'

    user_id = models.Column(models.Integer, primary_key = True, autoincrement = True)
    name = models.Column(models.String(50))


class User(db.Model):

    __tablename__ = "Users"

    id = models.Column(models.Integer, primary_key = True, autoincrement = True)
    fullname = models.Column(models.String(100), nullable = False)
    email_id = models.Column(models.String(100),  unique = True, nullable = False)
    password = models.Column(models.String(200), nullable = False)
    forms = db.relationship("W2Form", backref="user",lazy = True)

    def __repr__(self) -> str:
        return "{}-{}-{}".format(self.id, self.fullname, self.email_id)

    def is_active(self):
        return True

    def get_id(self):
        return self.id

    def is_authenticated(self):
        return self.authenticated

    def is_anonymous(self):
        return False

class W2Form(db.Model):

    __tablename__ = 'W2Forms'
    user_id = models.Column(models.Integer, models.ForeignKey('Users.id'), nullable = False)
    id = models.Column(models.Integer, primary_key = True, autoincrement = True)
    emp_social_num = models.Column(models.String(20), nullable = False)
    ein = models.Column(models.String(20), nullable = False)
    emp_address = models.Column(models.String(100), nullable = False)
    control_num = models.Column(models.String(20), nullable = False)

    def __repr__(self):
        return '<W2Form %r>' % self.id