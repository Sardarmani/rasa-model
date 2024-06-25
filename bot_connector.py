from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

@app.route('/send_reminder', methods=['POST'])
def send_reminder():
    data = request.json
    reminder_message = data.get('reminder_message')
    user_message = {
        "sender": "bot",
        "message": reminder_message
    }
    response = requests.post('http://localhost:5005/webhooks/rest/webhook', json=user_message)
    return jsonify(response.json())

if __name__ == '__main__':
    app.run(port=5002)
