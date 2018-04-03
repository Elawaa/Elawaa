import os
import sqlite3
from flask import Flask , request
from flask_restful import  Api ,reqparse, Resource
from flask import jsonify
#from security import authentication,identity
from flask_jwt import JWT, jwt_required, current_identity
#from werkzeug.security import safe_str_cmp
from sqlalchemy import create_engine,MetaData, Table
import datetime
from db import db
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy import update


DBSession = scoped_session(sessionmaker())
query = DBSession.query_property()
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///data.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_EXPIRATION_DELTA'] = datetime.timedelta(days=10)
app.secret_key = 'mahmoud'
app.config['DEBUG'] = True
#------------------------------------------------------------------

class users(db.Model):
    __tablename__ = 'users'
    d = db.Column(db.Integer, primary_key=True)
    id = db.Column(db.Integer)
    username = db.Column(db.Text(80))
    password = db.Column(db.Text(80))
    mail = db.Column(db.Text(80))
    carplate = db.Column(db.Text(80))
    phone = db.Column(db.Text(80))


class slotes(db.Model):
    __tablename__ = 'slotes'
    id = db.Column(db.Integer, primary_key=True)
    slote1 = db.Column(db.Text(80))
    slote2 = db.Column(db.Text(80))
    slote3 = db.Column(db.Text(80))
    slote4 = db.Column(db.Text(80))
#----------------------------------------------------------------

#UTHENTICATION


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
        #kwargs = {'username':username}
        #row = users.query.whoosh_search({'username':username})
        #row = users.query.filter_by(**kwargs).first()
        row = users.query.filter_by(username="'{}'".format(username)).first()
        if row:
            user = cls(row[0], row[1], row[2], row[3], row[4], row[5])
        else:
            user = None
        return user


    @classmethod                                                             # that is mean we use the current class so er replaces (self) with cls.
    def find_by_id(cls,id):
        result = users.query.filter_by(id="'{}'".format(id)).first()
        if result:
            user = cls(result[0], result[1], result[2], result[3], result[4], result[5])
        else:
            user = None

        return user





from werkzeug.security import safe_str_cmp


def authentication(username,password):                   #FILTER BY THE CARE PLTE BECAUSE IT NEVER REPEAT.
    user = userModel.find_by_username(username)
    if user and safe_str_cmp(user.password.encode('utf-8'), password.encode('utf-8')):
        return user
    return {'message': 'user not available'}


def identity(payload):
     user_id = payload['identity']
     return userModel.find_by_id(user_id)



jwt = JWT(app,authentication,identity)
#--------------------------------------------------------------------------













































def check_plate(carplate):
    result = users.query.filter_by(carplate=carplate).first()
    #row = result.fetchone()
    if result:
        return ("this plate is already excist"), 500







@app.route('/regs',methods=['post'])
def registeration():               # the first thing in the registration is the number of careplate.
    request_data = request.get_json()
    if not check_plate(request_data['carplate']):
        #User(username='admin', email='admin@example.com')
        a = users(id=request_data['id'], username=request_data['username'], password=request_data['password'], mail=request_data['mail'], carplate=request_data['carplate'], phone=request_data['phone'])
        db.session.add(a)
        db.session.commit()
        return jsonify({'user': request_data})

    else:
        return ("this plate is already excist"), 500






@app.route('/raspberry/carplates',methods=['GET'])                        #yyeeeeeeeeeeeeeeeeeeeeeeeeeeees.
#@jwt_required()
def get_slotes():
    #meta.Session.query(User).all()
    #result =meta.Session.query(users).all()
    result = users.query.all()
    #rows = result.fetchall()
    if result:
        carplates = []
        for row in result:
            carplates.append(row.carplate)
        return jsonify({'carplates': carplates})
    else:
        return None



@app.route('/slote/free',methods=['GET'])
#@jwt_required()
def get_free_slote():
    row = slotes.query.all()
    #row = result.fetchone()
    if row:
        for i in range(4):
            if (row.slote[i]) == -1:
            #if row[i] == -1:
                return jsonify({'free slote number': i})
        return ("No free slotes")
    #else:
    #   return jsonify({'message': None})




@app.route('/slote/userPosition/<string:id>',methods=['GET'])
@jwt_required()
def get_user_position(id,cls):
    result = slotes.query.all()
    row = result.first()
    if row:
        for i in range(4):
            if row[i] == int(id):
                return jsonify({'your position is': i})
            #return jsonify({'your': row, 'id':id})
        return jsonify({'message':'NO USER RELATED BY THIS ID'})
    #else:
    #    return jsonify({'message':None})



#@classmethod
@app.route('/raspberry/slote',methods=['put'])
#@jwt_required()
def updated():
    params_data = request.get_json()
    a = slotes(slote1=params_data[0], slote2=params_data[1], slote3=params_data[2], slote4=params_data[3])
    update(slotes).where(slotes.id==1).values(a)
    #result = slotes.update(a)
    row1 = slotes.query.first()
    #row1 = result1.fetchone()
    newRow = []
    for i in range(4):
        if (row1[i]) == 0:
            newRow.append(-1)
        else:
            newRow.append(row1[i])
    b = slotes(newRow[0], newRow[1], newRow[2], newRow[3],)
    update(slotes).where(slotes.id==1).values(b)
    row2 = slotes.query.first()
    #row2 = result2.fetchone()
    return jsonify({'garage_slotes':row2})



@classmethod
@app.route('/slote',methods=['put'])
@jwt_required()
def accept_user_position(cls):
    params_data = request.get_json()
    result = cls.slotes.query.all()
    row = result.fetchone()
    newRow = []
    for i in range(4):
        if int(params_data['sloteNumber']) == i:
            newRow.append(int(params_data['userId']))
        else:
            newRow.append(row[i])
    a = slotes(newRow[0],newRow[1],newRow[2],newRow[3],)
    db.session.update(a)
    db.session.commit()
    result = cls.slotes.query.all()
    row = result.fetchone()
    return jsonify({'garage_slotes':row})











@classmethod
@app.route('/users/remove',methods=['DELETE'])
@jwt_required()
def remove(cls):
    request_data = request.get_json()
    a= cls.users(str(request_data[0]),)
    db.session.delete(a)
    db.session.commit()
    #cursor.execute(delete,('A256',))                                 #if plate numbers and str ----->["plate number"]
    result = cls.users.query.all()
    row = result.fetchall()
    return jsonify({'users':row})






#if __name__ == '__main__':                                        #If condition to run the app only from the main .
#    app.run(port=5000, debug=True)

if __name__ == '__main__':
    from db import db
    db.init_app(app)

    if app.config['DEBUG']:
        @app.before_first_request
        def create_tables():
            db.create_all()

    app.run(port=5000)

