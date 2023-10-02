from flask import Flask, request, jsonify
import os
import sqlite3 
import datetime
from sense_hat import SenseHat

app = Flask(__name__)

dir = os.path.dirname(__file__)
db = os.path.join(dir, 'messages.db')

with sqlite3.connect(db) as connection:
    c = connection.cursor()
    c.execute('CREATE TABLE IF NOT EXISTS messages(id INTEGER PRIMARY KEY, type TEXT, color TEXT, content TEXT, datetime TEXT, sender_host TEXT, sender_name TEXT, receiever_host TEXT, receiever_name TEXT)')

app.config["JSON_AS_ASCII"] = False

sense = SenseHat()

r = (255, 0, 0)         # red
o = (255, 128, 0)       # orange
y = (255, 255, 0)       # yellow
g = (0, 255, 0)         # green
b = (0, 0, 255)         # blue
p = (255, 0, 255)       # purple
n = (255, 128, 128)     # pink
w = (255, 255, 255)     # white
k = (0, 0, 0)           # blank

# create POST endpoint to receive data and set LED matrix on sense hat to show message
@app.route('/set_message', methods=['POST'])
def set_message():
    if request.method == 'POST':
        type = request.json['type']
        color = request.json['color']
        content = request.json['content']
        current_datetime = datetime.datetime.now().replace(microsecond=0)
        current_datetime_str = current_datetime.strftime('%Y-%m-%d %H:%M:%S')
        sender_host = request.headers.get('Host')
        sender_name = request.json['sender_name']
        receiever_host = request.host
        receiever_name = request.json['receiever_name']

        with sqlite3.connect(db) as connection:
            c = connection.cursor()
            c.execute('INSERT INTO messages(type, color, content, datetime, sender_host, sender_name, receiever_host, receiever_name) VALUES(?, ?, ?, ?, ?, ?, ?, ?)', (type, color, content, current_datetime_str, sender_host, sender_name, receiever_host, receiever_name))

        if color == "blue":
            c = b
        elif color == "green":
            c = g
        elif color == "yellow":
            c = y
        elif color == "red":
            c = r
        elif color == "pink":
            c = n

        if type == "message":
            sense.show_message(content, 0.1, c)
            # return json response with OK status
            return jsonify({'status': 'Message set', 'type': type, 'color': color, 'message': content, 'sender_name': sender_name, 'receiever_name': receiever_name})
        elif type == "heart":
            sense.set_pixels([
                k, c, c, k, k, c, c, k,
                c, c, c, c, c, c, c, c,
                c, c, c, c, c, c, c, c,
                c, c, c, c, c, c, c, c,
                c, c, c, c, c, c, c, c,
                k, c, c, c, c, c, c, k,
                k, k, c, c, c, c, k, k,
                k, k, k, c, c, k, k, k
            ])
            # return json response with OK status
            return jsonify({'status': 'Heart set', 'type': type, 'color': color, 'sender_name': sender_name, 'receiever_name': receiever_name})
        elif type == "smiley":
            if content == "happy":
                sense.set_pixels([
                    k, k, k, k, k, k, k, k,
                    k, c, c, k, k, c, c, k,
                    k, c, c, k, k, c, c, k,
                    k, k, k, k, k, k, k, k,
                    c, c, k, k, k, k, c, c,
                    c, c, c, c, c, c, c, c,
                    k, c, c, c, c, c, c, k,
                    k, k, k, k, k, k, k, k])
                # return json response with OK status
                return jsonify({'status': 'Smiley set', 'type': type, 'color': color, 'mood': content, 'sender_name': sender_name, 'receiever_name': receiever_name})
            elif content == "sad":
                sense.set_pixels([
                    k, k, k, k, k, k, k, k,
                    k, c, c, k, k, c, c, k,
                    k, c, c, k, k, c, c, k,
                    k, k, k, k, k, k, k, k,
                    k, k, k, k, k, k, k, k,
                    k, c, c, c, c, c, c, k,
                    c, c, c, c, c, c, c, c,
                    c, c, k, k, k, k, c, c])
                # return json response with OK status
                return jsonify({'status': 'Smiley set', 'type': type, 'color': color, 'mood': content, 'sender_name': sender_name, 'receiever_name': receiever_name})
            else:
                sense.clear()
                return jsonify({'status': 'No smiley set', 'type': type, 'color': color, 'mood': 'Only happy or sad accepted as content', 'sender_name': sender_name, 'receiever_name': receiever_name})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)

# show me example curl requests to set_message endpoint

# curl -X POST -H "Content-Type: application/json" -d '{"type": "message", "color": "blue", "content": "Hello World", "sender_name": "Mikkel", "receiever_name": "Bob"}' http://beitpi.local:8000/set_message
# curl -X POST -H "Content-Type: application/json" -d '{"type": "heart", "color": "pink", "content": "", "sender_name": "Mikkel", "receiever_name": "Bob"}' http://beitpi.local:8000/set_message
# curl -X POST -H "Content-Type: application/json" -d '{"type": "smiley", "color": "yellow", "content": "happy", "sender_name": "Mikkel", "receiever_name": "Bob"}' http://beitpi.local:8000/set_message
