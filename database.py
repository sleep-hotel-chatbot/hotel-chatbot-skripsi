import os

def get_db_connection():
    """Get database connection with fallback"""
    database_url = os.environ.get('DATABASE_URL')
    
    print(f"🔧 Environment check - DATABASE_URL: {bool(database_url)}")
    
    # Try PostgreSQL first (for Railway)
    if database_url:
        try:
            import psycopg2
            print("🐘 Attempting PostgreSQL connection...")
            conn = psycopg2.connect(database_url)
            print("✅ Connected to PostgreSQL")
            return conn, 'postgresql'
        except Exception as e:
            print(f"⚠️ PostgreSQL failed: {e}")
    
    # Fallback to SQLite
    try:
        import sqlite3
        print("📁 Using SQLite fallback")
        conn = sqlite3.connect('hotel_data.db')
        return conn, 'sqlite'
    except Exception as e:
        print(f"❌ SQLite also failed: {e}")
        return None, None

def init_database():
    """Initialize database"""
    conn, db_type = get_db_connection()
    if not conn:
        print("❌ Cannot connect to any database")
        return
    
    cursor = conn.cursor()
    
    try:
        if db_type == 'postgresql':
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS rooms (
                    id SERIAL PRIMARY KEY,
                    gender VARCHAR(10),
                    level INTEGER,
                    available INTEGER,
                    total INTEGER,
                    price INTEGER
                )
            ''')
            
            # Clear and insert
            cursor.execute('DELETE FROM rooms')
            rooms_data = [
                ('pria', 1, 3, 10, 65000),
                ('pria', 2, 5, 15, 55000),
                ('wanita', 1, 2, 8, 65000),
                ('wanita', 2, 4, 12, 55000)
            ]
            
            for room in rooms_data:
                cursor.execute(
                    'INSERT INTO rooms (gender, level, available, total, price) VALUES (%s, %s, %s, %s, %s)',
                    room
                )
            
            print("✅ PostgreSQL initialized")
            
        else:  # SQLite
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS rooms (
                    id INTEGER PRIMARY KEY,
                    gender TEXT,
                    level INTEGER,
                    available INTEGER,
                    total INTEGER,
                    price INTEGER
                )
            ''')
            
            cursor.execute('DELETE FROM rooms')
            rooms_data = [
                (1, 'pria', 1, 3, 10, 65000),
                (2, 'pria', 2, 5, 15, 55000),
                (3, 'wanita', 1, 2, 8, 65000),
                (4, 'wanita', 2, 4, 12, 55000)
            ]
            
            cursor.executemany(
                'INSERT INTO rooms VALUES (?, ?, ?, ?, ?, ?)',
                rooms_data
            )
            
            print("✅ SQLite initialized")
        
        conn.commit()
        
    except Exception as e:
        print(f"❌ Database init error: {e}")
        conn.rollback()
    finally:
        cursor.close()
        conn.close()

def get_room_availability():
    """Get room data"""
    conn, db_type = get_db_connection()
    if not conn:
        return []
    
    cursor = conn.cursor()
    
    try:
        cursor.execute('SELECT gender, level, available FROM rooms ORDER BY gender, level')
        rows = cursor.fetchall()
        
        result = []
        for row in rows:
            result.append({
                'gender': row[0],
                'level': row[1],
                'available': row[2]
            })
        
        return result
    except Exception as e:
        print(f"❌ Query error: {e}")
        return []
    finally:
        cursor.close()
        conn.close()