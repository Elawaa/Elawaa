import sqlite3
from flask_jwt import JWT, jwt_required, current_identity
from werkzeug.security import safe_str_cmp

#from user import userModel

class userModel():
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







def authentication(username,password):                   #FILTER BY THE CARE PLTE BECAUSE IT NEVER REPEAT.
    user = userModel.find_by_username(username)
    if user and safe_str_cmp(user.password.encode('utf-8'), password.encode('utf-8')):
        return user
    return {'message': 'user not available'}


def identity(payload):
     user_id = payload['identity']
     return userModel.find_by_id(user_id)





