from flask import Flask, request, jsonify, make_response, abort
from werkzeug.security import generate_password_hash, check_password_hash
from globalSettings import *
from functools import wraps
import jwt
import datetime
from models import *


app = Flask(__name__)

@app.errorhandler(400)
def malformedRequest(error):
    return make_response(jsonify({'Error': 'request must be JSON'}, 400)) 

@app.errorhandler(404)
def malformedRequest(error):
    return make_response(jsonify({'Error': 'Object not found on the server'}, 400))

@app.errorhandler(415)
def notFoundError(error):
    return make_response(jsonify({'Error': 'Not found'}, 404))

def tokenRequired(f):
   @wraps(f)
   def decorator(*args, **kwargs):
       token = None
       if 'x-access-tokens' in request.headers:
           token = request.headers['x-access-tokens']

       if not token:
           return jsonify({'Message': 'a valid token is missing'})
       try:
           data = jwt.decode(token, str(app.secret_key), algorithms=["HS256"])
           currentUser = session.query(User).\
               filter(User.id==data['id']).\
               first()
       except:
           return jsonify({'Message': 'token is invalid'})
 
       return f(currentUser, *args, **kwargs)
   return decorator

@app.post('/register')
def register():
    registerData = request.get_json()
    print(registerData)
    hashedPassword = generate_password_hash(registerData['password'], method='sha256')

    user = User(registerData['username'], hashedPassword)
    session.add(user)
    session.commit()

    return make_response(jsonify({'Message': 'New user created successfully'}, 201))

@app.post('/login') 
def login():    
    auth = request.authorization  
    
    if not auth or not auth.username or not auth.password: 
        return make_response('Could not verify', 401, {'Authentication': 'login required"'})   
    
    user = session.query(User).\
        filter(User.username==auth.username).\
        first()  
   
    if check_password_hash(user.password, auth.password):
        token = jwt.encode({'id' : user.id, 'exp' : datetime.datetime.utcnow() + datetime.timedelta(minutes=45)}, str(app.secret_key), "HS256")

        return jsonify({'token' : token})
    
    return make_response('could not verify',  401, {'Authentication': '"login required"'})

@app.get('/players')
@tokenRequired
def getPlayers(currentUser):
    return make_response(jsonify({'players': getAllPlayers()}, 200))

def getAllPlayers():
    return session.query(Player).all()

@app.get('/players/<id>')
@tokenRequired
def getPlayer(currentUser, id):
    return make_response(jsonify({'player': getOnePlayer(id)}, 200))

def getOnePlayer(id):
    player = session.query(Player).\
        filter(Player.id == id).\
        first()
    if(player == None):
        abort(404)

    return player

@app.post("/players")
@tokenRequired
def addPlayer(currentUser):
    if(request.is_json):
        player = request.get_json(force=True)

        saveNewPlayer(player)

        return make_response(jsonify({'player': request.get_json()}, 201))

    return abort(415)

def saveNewPlayer(player):
    player = Player(player['name'],\
        player['surname'],\
        player['age'],\
        player['nationality'],\
        player['club'])
    session.add(player)
    session.commit()

@app.put('/players/<id>')
@tokenRequired
def updatePlayer(currentUser, id):
    if(request.is_json):
        player = request.get_json(force=True)

        updateExistingPlayer(id, player)

        return make_response(jsonify({'player': request.get_json()}, 200))

    return abort(415)

def updateExistingPlayer(id, player):
    name = player['name']
    surname = player['surname']
    age = player['age']
    nationality = player['nationality']
    club = player['club']

    session.query(Player).\
        filter(Player.id==id).\
        update({'id': id,\
            'name': name,\
            'surname': surname,\
            'age': age,\
            'nationality': nationality,\
            'club': club},\
            synchronize_session='fetch')
    session.commit()


@app.delete('/players/<id>')
@tokenRequired
def deletePlayer(currentUser, id):
    deletePlayerFromDb(id)
    print()
    return make_response(jsonify({'Message': f'User under id {id}, deleted successfully.'}, 200))

def deletePlayerFromDb(id):
    session.query(Player).\
        filter(Player.id==id).\
        delete()
    session.commit()



if __name__ == '__main__':
    app.run()
   