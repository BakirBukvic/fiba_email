import sys
import os
from datetime import datetime

# Add the parent directory to the path to access db module
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, parent_dir)

from get_events.get_events import get_events
from db.make_db import insert_event, create_database, get_existing_event_ids

def store_events_to_db():
    """
    Fetch events and store them to database.
    Detects new events and prints notification when new ones are found.
    """
    # Ensure database exists
    create_database()
    
    # Get existing event IDs before scraping
    existing_event_ids = get_existing_event_ids()
    print(f"Found {len(existing_event_ids)} existing events in database")
    
    # Get the events data from API
    events_data = get_events()
    
    # Extract the results array
    events = events_data.get('results', [])
    print(f"Retrieved {len(events)} events from API")
    
    # Current scraping date
    scrape_date = datetime.now().strftime("%Y-%m-%d")
    
    # Track new events and missing events
    new_events = []
    missing_events = []
    current_event_ids = set()
    
    # Store each event in the database
    stored_count = 0
    for event in events:
        try:
            event_id = event['id']
            current_event_ids.add(event_id)
            
            # Check if this is a new event
            if event_id not in existing_event_ids:
                new_events.append(event)
            
            # Extract fields we need for our database
            event_record = {
                'id': event_id,
                'name': event['name'],
                'registrationIsOpen': event['registrationIsOpen'],
                'startDate': event['startDate'],
                'endDate': event['endDate'],
                'city': event['city'],
                'date_scraped': scrape_date
            }
            
            insert_event(event_record)
            stored_count += 1
            print(f"Stored event: {event['name']} in {event['city']}")
            
        except KeyError as e:
            print(f"Missing field {e} in event: {event.get('id', 'unknown')}")
        except Exception as e:
            print(f"Error storing event {event.get('id', 'unknown')}: {e}")
    
    # Check for missing events (events in database but not in current API response)
    missing_event_ids = existing_event_ids - current_event_ids
    if missing_event_ids:
        # Get details of missing events from database
        from db.make_db import get_db_connection
        conn = get_db_connection()
        cursor = conn.cursor()
        
        for missing_id in missing_event_ids:
            cursor.execute('''
                SELECT id, name, registrationIsOpen, startDate, endDate, city, date_scraped
                FROM events WHERE id = ?
            ''', (missing_id,))
            event_data = cursor.fetchone()
            if event_data:
                missing_events.append({
                    'id': event_data[0],
                    'name': event_data[1],
                    'registrationIsOpen': event_data[2],
                    'startDate': event_data[3],
                    'endDate': event_data[4],
                    'city': event_data[5],
                    'date_scraped': event_data[6]
                })
        
        conn.close()
    
    # Report on new events found
    if new_events:
        print(f"\n🎉 NEW EVENTS DETECTED ({len(new_events)}):")
        for event in new_events:
            reg_status = "🟢 OPEN" if event['registrationIsOpen'] else "🔴 CLOSED"
            print(f"   • {event['name']} in {event['city']} - {reg_status}")
            print(f"     📅 {event['startDate'][:10]} to {event['endDate'][:10]}")
        print("\n📧 [NOTIFICATION NEEDED] - Send notification about new events")
    
    # Report on missing events
    if missing_events:
        print(f"\n⚠️  MISSING EVENTS DETECTED ({len(missing_events)}):")
        print("   Events that were in database but not found in current API response:")
        for event in missing_events:
            reg_status = "🟢 OPEN" if event['registrationIsOpen'] else "🔴 CLOSED"
            print(f"   • {event['name']} in {event['city']} - {reg_status}")
            print(f"     📅 {event['startDate'][:10]} to {event['endDate'][:10]}")
            print(f"     🕒 Last scraped: {event['date_scraped']}")
        print("\n📧 [NOTIFICATION NEEDED] - Send notification about missing events")
    
    # Summary message
    if not new_events and not missing_events:
        print(f"\n✅ No new or missing events found since last scrape")
    
    print(f"\n📊 Summary:")
    print(f"   • Total events from API: {len(events)}")
    print(f"   • Events stored to database: {stored_count}")
    print(f"   • New events detected: {len(new_events)}")
    print(f"   • Missing events detected: {len(missing_events)}")
    print(f"   • Scrape date: {scrape_date}")
    
    return {
        'events_data': events_data,
        'new_events': new_events,
        'missing_events': missing_events,
        'summary': {
            'total_api_events': len(events),
            'stored_count': stored_count,
            'new_count': len(new_events),
            'missing_count': len(missing_events),
            'scrape_date': scrape_date
        }
    }

if __name__ == "__main__":
    store_events_to_db()
