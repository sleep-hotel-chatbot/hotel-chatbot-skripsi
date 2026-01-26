import os
import logging

def get_db_connection():
    """Get database connection (SQLite for local, PostgreSQL for Railway)"""
    database_url = os.environ.get('DATABASE_URL')
    
    # If no DATABASE_URL (local development), use SQLite
    if not database_url:
        try:
            import sqlite3
            conn = sqlite3.connect('hotel_data.db')
            print("📁 Using SQLite database (local development)")
            return conn, 'sqlite'
        except ImportError:
            print("❌ SQLite not available")
            return None, None
    
    # If DATABASE_URL exists (Railway), use PostgreSQL
    try:
        import psycopg2
        # Railway requires SSL
        conn = psycopg2.connect(database_url, sslmode='require')
        print("🐘 Using PostgreSQL database (Railway)")
        return conn, 'postgresql'
    except ImportError:
        print("❌ psycopg2 not installed, falling back to SQLite")
        import sqlite3
        return sqlite3.connect('hotel_data.db'), 'sqlite'

def init_database():
    """Initialize database with hotel room data"""
    conn, db_type = get_db_connection()
    if not conn:
        print("❌ Failed to connect to database")
        return
    
    cursor = conn.cursor()
    
    try:
        if db_type == 'postgresql':
            # PostgreSQL schema
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS rooms (
                    id SERIAL PRIMARY KEY,
                    gender VARCHAR(10) NOT NULL,
                    level INTEGER NOT NULL,
                    available INTEGER,
                    total INTEGER,
                    price INTEGER
                )
            ''')
            
            # Clear and insert fresh data
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
            
            print("✅ PostgreSQL database initialized with sample data")
            
        else:  # SQLite
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
            
            # Clear and insert fresh data
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
            
            print("✅ SQLite database initialized with sample data")
        
        conn.commit()
        
    except Exception as e:
        print(f"❌ Database initialization error: {e}")
        conn.rollback()
        
    finally:
        cursor.close()
        conn.close()

def get_room_availability():
    """Get all room availability data"""
    conn, db_type = get_db_connection()
    if not conn:
        return []
    
    cursor = conn.cursor()
    
    try:
        if db_type == 'postgresql':
            cursor.execute('SELECT gender, level, available, total, price FROM rooms ORDER BY gender, level')
        else:
            cursor.execute('SELECT gender, level, available, total, price FROM rooms ORDER BY gender, level')
        
        rooms = cursor.fetchall()
        
        # Format results
        result = []
        for room in rooms:
            result.append({
                'gender': room[0],
                'level': room[1],
                'available': room[2],
                'total': room[3],
                'price': room[4]
            })
        
        return result
        
    except Exception as e:
        print(f"❌ Error fetching room data: {e}")
        return []
        
    finally:
        cursor.close()
        conn.close()