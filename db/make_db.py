import sqlite3
import os
from datetime import datetime

def create_database():
    """
    Creates the SQLite database and events table if they don't exist.
    This function is safe to run multiple times.
    """
    # Get the directory where this script is located
    db_dir = os.path.dirname(os.path.abspath(__file__))
    db_path = os.path.join(db_dir, 'events.db')
    
    # Connect to SQLite database (creates file if it doesn't exist)
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Create events table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS events (
            id TEXT PRIMARY KEY,
            name TEXT NOT NULL,
            registrationIsOpen BOOLEAN NOT NULL,
            startDate TEXT NOT NULL,
            endDate TEXT NOT NULL,
            city TEXT NOT NULL,
            date_scraped TEXT NOT NULL,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP,
            updated_at TEXT DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Create an index on startDate for faster queries
    cursor.execute('''
        CREATE INDEX IF NOT EXISTS idx_events_start_date ON events(startDate)
    ''')
    
    # Create an index on registrationIsOpen for faster filtering
    cursor.execute('''
        CREATE INDEX IF NOT EXISTS idx_events_registration ON events(registrationIsOpen)
    ''')
    
    # Commit changes and close connection
    conn.commit()
    conn.close()
    
    print(f"Database created successfully at: {db_path}")
    return db_path

def get_db_connection():
    """
    Returns a connection to the events database.
    Creates the database if it doesn't exist.
    """
    db_dir = os.path.dirname(os.path.abspath(__file__))
    db_path = os.path.join(db_dir, 'events.db')
    
    if not os.path.exists(db_path):
        create_database()
    
    return sqlite3.connect(db_path)

def insert_event(event_data):
    """
    Insert or update an event in the database.
    Uses INSERT OR REPLACE to handle duplicates.
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute('''
        INSERT OR REPLACE INTO events 
        (id, name, registrationIsOpen, startDate, endDate, city, date_scraped, updated_at)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    ''', (
        event_data['id'],
        event_data['name'],
        event_data['registrationIsOpen'],
        event_data['startDate'],
        event_data['endDate'],
        event_data['city'],
        event_data['date_scraped'],
        datetime.now().isoformat()
    ))
    
    conn.commit()
    conn.close()

def get_all_events():
    """
    Retrieve all events from the database.
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute('''
        SELECT id, name, registrationIsOpen, startDate, endDate, city, 
               date_scraped, created_at, updated_at 
        FROM events 
        ORDER BY startDate
    ''')
    
    events = cursor.fetchall()
    conn.close()
    
    return events

def get_open_registrations():
    """
    Get events with open registration.
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute('''
        SELECT id, name, registrationIsOpen, startDate, endDate, city, 
               date_scraped, created_at, updated_at 
        FROM events 
        WHERE registrationIsOpen = 1
        ORDER BY startDate
    ''')
    
    events = cursor.fetchall()
    conn.close()
    
    return events

def get_existing_event_ids():
    """
    Get all existing event IDs from the database.
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute('SELECT id FROM events')
    result = cursor.fetchall()
    conn.close()
    
    return {row[0] for row in result}  # Return as a set for fast lookup

if __name__ == "__main__":
    # Create the database and table
    db_path = create_database()
    print("Database setup completed!")
    
    # Test the connection
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='events'")
        result = cursor.fetchone()
        conn.close()
        
        if result:
            print("✓ Events table created successfully")
        else:
            print("✗ Events table not found")
    except Exception as e:
        print(f"✗ Error testing database: {e}")
