# Smart Home project

Raspberry Pi with Flask application and SQLite database showing messages on Sense HAT.

## cURL requests

Change hostname to the one for your Raspberry Pi. The Flask application is running on port 8000.

```
curl -X POST -H "Content-Type: application/json" -d '{"type": "message", "color": "blue", "content": "Hello World", "sender_name": "Mikkel", "receiever_name": "Bob"}' http://hostname.local:8000/set_message'''

curl -X POST -H "Content-Type: application/json" -d '{"type": "heart", "color": "pink", "content": "", "sender_name": "Mikkel", "receiever_name": "Bob"}' http://hostname.local:8000/set_message

curl -X POST -H "Content-Type: application/json" -d '{"type": "smiley", "color": "yellow", "content": "happy", "sender_name": "Mikkel", "receiever_name": "Bob"}' http://hostname.local:8000/set_message
```
