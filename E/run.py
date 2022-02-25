from numpy import broadcast
from modules import app, db
from flask_socketio import SocketIO, send
import datetime
from modules.models import User, Message

socketio = SocketIO(app, cors_allowed_origins='*')

for i in range(1, 10):
    for j in range(i + 1, 11):
        if i != j:
            @socketio.on("message", namespace=f'/chat/{i}/{j}')
            def handleMessage(msg):
                x = datetime.datetime.now()
                currentTime = str(x.strftime("%d")) + " " + str(x.strftime("%b")) + " " + str(x.strftime("%y")) + " " + str(x.strftime("%I")) + ":" + str(x.strftime("%M")) + " " + str(x.strftime("%p"))
                
                message_packet = msg.split('----')
                message = message_packet[0]
                sender = message_packet[1]
                receiver = message_packet[2]

                new_message = Message(message=message, sender=sender, receiver=receiver, message_stamp=currentTime)
                db.session.add(new_message)
                db.session.commit()
                send(msg, broadcast=True)

if __name__ == '__main__':
    app.run(debug=True)