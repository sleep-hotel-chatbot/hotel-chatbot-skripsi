from flask import Flask, request, jsonify
import sqlite3
import json
import os

app = Flask(__name__)

# ==================== DATABASE FUNCTIONS ====================
def init_database():
    """Initialize SQLite database with hotel data"""
    try:
        conn = sqlite3.connect('hotel_data.db')
        cursor = conn.cursor()
        
        # Create rooms table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS rooms (
                id INTEGER PRIMARY KEY,
                gender TEXT NOT NULL,
                level INTEGER NOT NULL,
                available INTEGER,
                total INTEGER,
                price INTEGER
            )
        ''')
        
        # Insert sample data
        rooms_data = [
            (1, 'pria', 1, 3, 10, 65000),
            (2, 'pria', 2, 5, 15, 55000),
            (3, 'wanita', 1, 2, 8, 65000),
            (4, 'wanita', 2, 4, 12, 55000)
        ]
        
        cursor.executemany('''
            INSERT OR REPLACE INTO rooms (id, gender, level, available, total, price)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', rooms_data)
        
        conn.commit()
        conn.close()
        print("✅ Database initialized successfully!")
        
    except Exception as e:
        print(f"❌ Database error: {e}")

# ==================== WEBHOOK HANDLER ====================
@app.route('/webhook', methods=['POST'])
def webhook():
    """Main webhook endpoint for Dialogflow"""
    try:
        req = request.get_json()
        print("📨 Received request:", json.dumps(req, indent=2))
        
        # Get intent name
        intent_name = req.get('queryResult', {}).get('intent', {}).get('displayName', '')
        
        # Handle different intents
        if intent_name == 'TestConnection':
            response_text = '✅ Bot berhasil terkoneksi! Sistem siap membantu.'
        
        elif intent_name == 'MainMenu':
            response_text = '🏨 SLEEP AND SLEEP CAPSULE HOTEL\n\nHalo! Ada yang bisa saya bantu?\n\nSilakan pilih menu:'
            # Nanti kita tambahkan buttons di sini
        
        elif intent_name == 'CheckRoomAvailability':
            response_text = '🛌 KETERSEDIAAN KAMAR\n\nBerdasarkan data terakhir:\n• Pria Level 1: 3 bed\n• Pria Level 2: 5 bed\n• Wanita Level 1: 2 bed\n• Wanita Level 2: 4 bed\n\n💡 Untuk konfirmasi real-time: 📞 021-1234567'
        
        else:
            response_text = 'Maaf, saya belum bisa menjawab pertanyaan itu. Silakan gunakan menu yang tersedia.'
        
        # Return response
        return jsonify({
            'fulfillmentText': response_text
        })
        
    except Exception as e:
        print(f"❌ Webhook error: {e}")
        return jsonify({
            'fulfillmentText': f'Maaf, terjadi error: {str(e)}'
        })

# ==================== HOME PAGE ====================
@app.route('/')
def home():
    return '''
    <h1>🏨 Sleep and Sleep Capsule Chatbot API</h1>
    <p>Webhook is running successfully!</p>
    <p>Test endpoint: POST /webhook</p>
    '''

# ==================== MAIN EXECUTION ====================
if __name__ == '__main__':
    print("🚀 Initializing Hotel Chatbot System...")
    init_database()
    print("🌐 Server starting at http://localhost:5000")
    app.run(debug=True, port=5000)