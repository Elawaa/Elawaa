import sqlite3
from db import db


"""
class slotes(db.Model):
    __tablename__ = 'slotes'
    id = db.Column(db.Integer, primary_key=True)
    slote1 = db.Column(db.Text(80))
    slote2 = db.Column(db.Text(80))
    slote3 = db.Column(db.Text(80))
    slote4 = db.Column(db.Text(80))


class users(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    Id = db.Column(db.Integer)
    username = db.Column(db.Text(80))
    password = db.Column(db.Text(80))
    mail = db.Column(db.Text(80))
    carplate = db.Column(db.Text(80))
    phone = db.Column(db.Text(80))


"""





class userModel():
    """__tablename__ = 'slotes'
    id = db.Column(db.Integer, primary_key=True)
    slote1 = db.Column(db.Text(80))
    slote2 = db.Column(db.Text(80))
    slote3 = db.Column(db.Text(80))
    slote4 = db.Column(db.Text(80))


    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    Id = db.Column(db.Integer)
    username = db.Column(db.Text(80))
    password = db.Column(db.Text(80))
    mail = db.Column(db.Text(80))
    carplate = db.Column(db.Text(80))
    phone = db.Column(db.Text(80))"""




    def __init__(self, id, username, password, mail, carplate, phone):                               #there is a(_)before id because it already a basic element in a python.
        self.id = id
        self.username = username
        self.password = password
        self.mail = mail
        self.carplate = carplate
        self.phone = phone

    @classmethod                                                            #that is mean we use the current class so er replaces (self) with cls.
    def find_by_username(cls,username):
        row = users.query.filter_by(username=username).first()
        #row = result.fetchone()
        if row:
            user = cls(row[0], row[1], row[2], row[3], row[4], row[5])
        else:
            user= None
        return user




    @classmethod                                                             # that is mean we use the current class so er replaces (self) with cls.
    def find_by_id(cls, id):
        row = users.query.filter_by(Id=id).first()
        #row = result.fetchone()
        if row:
            user = cls(row[0], row[1], row[2], row[3], row[4], row[5])
        else:
            user = None

        return user

