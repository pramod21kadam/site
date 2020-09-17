from packages.flaskPackages import *
from service._init_ import *
from .base import *
import utilities.globals as Global
import init


socketio = init.socketio

@socketio.on("connect")
def conntect():
    # SocketServ().connect(request.remote_addr)
    Global.online += 1
    emit("online", Global.online, broadcast = True)
    try:
        print (f"{(request.sid)} connected the room with ip {request.remote_addr}")
    except Exception as e:
        print(e)

@socketio.on("disconnect")
def disconnect():
    Global.online -= 1

    # SocketServ().disconnect(request.remote_addr)

    if len(Global.clients) == 0:
        room, boolean = searchPartner(request.sid, Global.rooms)
        if(boolean):
            Global.rooms.remove(room)
            room.remove(request.sid)
            emit('left_chat', room = room[0])
    else:
        Global.clients = []
    emit("online", Global.online, broadcast = True)
    print(f"{request.sid} disconnected with ip {request.remote_addr}")

@socketio.on("partner")
def search():
    try:
        print(f"partner search for {request.sid}")
        if len(Global.clients) != 0 and Global.clients[0] != request.sid:
            emit("partner", request.sid, room = Global.clients[0])
            emit("partner", Global.clients[0], room = request.sid)
            Global.rooms.append([request.sid, Global.clients[0]])
            Global.clients.pop()
            print("Created room")
        else:
            Global.clients.append(request.sid)
    except Exception as e:
        print(e)

@socketio.on('message')
def handleMessage(data):
    emit('message', data, room = data['to'])

@socketio.on('leave_room')
def leave_room(data):
    if data['partner'] != None:
        emit('leave_room', room=data['partner'])
    
@socketio.on('typing')
def typing(data):
    emit('typing',room = data['partner'])