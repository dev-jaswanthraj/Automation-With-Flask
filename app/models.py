from turtle import mode
from .extensions import db
import sqlalchemy as models

class TestTable(db.Model):
    __tabelname__ = 'Tests'

    user_id = models.Column(models.Integer, primary_key = True, autoincrement = True)
    name = models.Column(models.String(50))

class W2Form(db.Model):

    __tabelname__ = 'W2Forms'
    
    id = models.Column(models.Integer, primary_key = True, autoincrement = True)
    emp_social_num = models.Column(models.String(20), nullable = False)
    ein = models.Column(models.String(20), nullable = False)
    emp_address = models.Column(models.String(100), nullable = False)
    control_num = models.Column(models.String(20), nullable = False)

    def __repr__(self):
        return '<W2Form %r>' % self.id


