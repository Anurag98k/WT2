from Project import db # It should be from Project import db
from sqlalchemy.schema import PrimaryKeyConstraint

#Yet to be filled, fields are incorrect
class Electives(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))

    def __repr__(self):
        return '<Elective {}>'.format(self.username)    
