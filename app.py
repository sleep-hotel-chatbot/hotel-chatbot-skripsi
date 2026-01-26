from flask import Flask, request, jsonify
from database import init_database, get_room_availability
import json
import os

app = Flask(__name__)

@app.route('/webhook', methods=['POST'])
def webhook():
    try:
        req = request.get_json()
        intent_name = req.get('queryResult', {}).get('intent', {}).get('displayName', '')
        
        if intent_name == 'TestConnection':
            response_text = '✅ Bot berhasil terkoneksi! Sistem siap membantu.'
        
        elif intent_name == 'MainMenu':
            response_text = '🏨 SLEEP AND SLEEP CAPSULE HOTEL\n\nHalo! Ada yang bisa saya bantu?\n\nSilakan pilih menu:'
        
        elif intent_name == 'CheckRoomAvailability':
            rooms = get_room_availability()
            response_text = '🛌 KETERSEDIAAN KAMAR\n\n'
            pria_rooms = [r for r in rooms if r['gender'] == 'pria']
            wanita_rooms = [r for r in rooms if r['gender'] == 'wanita']
            
            if pria_rooms:
                response_text += '👨 KAMAR PRIA:\n'
                for room in pria_rooms:
                    response_text += f'• Level {room["level"]}: {room["available"]} bed tersedia\n'
            
            if wanita_rooms:
                response_text += '\n👩 KAMAR WANITA:\n'
                for room in wanita_rooms:
                    response_text += f'• Level {room["level"]}: {room["available"]} bed tersedia\n'
            
            response_text += '\n💡 Untuk konfirmasi real-time: 📞 021-1234567'
        
        else:
            response_text = 'Maaf, saya belum bisa menjawab pertanyaan itu. Silakan gunakan menu yang tersedia.'
        
        return jsonify({'fulfillmentText': response_text})
        
    except Exception as e:
        return jsonify({'fulfillmentText': f'Maaf, terjadi error: {str(e)}'})

@app.route('/')
def home():
    return '''
    <h1>🏨 Sleep and Sleep Capsule Chatbot API</h1>
    <p>Webhook is running successfully!</p>
    <p>Test endpoint: POST /webhook</p>
    '''

if __name__ == '__main__':
    print("🚀 Initializing Hotel Chatbot System...")
    init_database()
    print("🌐 Server starting at http://localhost:5000")
    app.run(debug=True, port=5000)