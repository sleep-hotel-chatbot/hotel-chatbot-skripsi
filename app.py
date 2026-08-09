from flask import Flask, request, jsonify
import os

app = Flask(__name__)

@app.route('/webhook', methods=['POST', 'GET'])
def webhook():
    try:
        # Untuk GET request (test browser)
        if request.method == 'GET':
            return jsonify({'message': '✅ Webhook is ready! Use POST method.'})
        
        # Untuk POST request (dari Dialogflow)
        data = request.get_json()
        print("📨 Received:", data)
        
        # Ambil intent name
        intent = data.get('queryResult', {}).get('intent', {}).get('displayName', '')
        
        # Response berdasarkan intent
        if intent == 'TestConnection':
            text = '✅ Bot berhasil terkoneksi! Sistem siap membantu.'
        elif intent == 'MainMenu':
            text = '🏨 SELAMAT DATANG DI SLEEP AND SLEEP CAPSULE!\n\nSilakan pilih menu:\n[ℹ️ INFO] [🛌 KAMAR] [📍 REKOMENDASI]'
        elif intent == 'CheckRoomAvailability':
            text = '🛌 KETERSEDIAAN KAMAR\n\n👨 KAMAR PRIA:\n• Level 1: 3 bed tersedia\n• Level 2: 5 bed tersedia\n\n👩 KAMAR WANITA:\n• Level 1: 2 bed tersedia\n• Level 2: 4 bed tersedia\n\n📞 021-1234567 untuk info lebih lanjut'
        else:
            text = 'Maaf, saya belum bisa menjawab pertanyaan itu. Silakan gunakan menu yang tersedia.'
        
        return jsonify({'fulfillmentText': text})
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return jsonify({'fulfillmentText': f'Maaf, terjadi error: {str(e)}'})

@app.route('/')
def home():
    return '''
    <h1>🏨 Sleep and Sleep Capsule Chatbot API</h1>
    <p>✅ Webhook berjalan!</p>
    <p>Test: POST /webhook</p>
    '''

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    print(f"🚀 Server starting on port {port}")
    app.run(host='0.0.0.0', port=port, debug=False)