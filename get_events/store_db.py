import sys
import os

# Add the parent directory to the path to access db module
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, parent_dir)

from get_events.get_events import get_events
from db.make_db import insert_event, create_database

def store_events_to_db():
    """
    Fetch events and store them to database
    """
    # Ensure database exists
    create_database()
    
    # Get the events data
    events_data = get_events()
    
    # Extract the results array
    events = events_data.get('results', [])
    print(f"Retrieved {len(events)} events")
    
    # Store each event in the database
    stored_count = 0
    for event in events:
        try:
            # Extract only the fields we need for our database
            event_record = {
                'id': event['id'],
                'name': event['name'],
                'registrationIsOpen': event['registrationIsOpen'],
                'startDate': event['startDate'],
                'endDate': event['endDate'],
                'city': event['city']
            }
            
            insert_event(event_record)
            stored_count += 1
            print(f"Stored event: {event['name']} in {event['city']}")
            
        except KeyError as e:
            print(f"Missing field {e} in event: {event.get('id', 'unknown')}")
        except Exception as e:
            print(f"Error storing event {event.get('id', 'unknown')}: {e}")
    
    print(f"Successfully stored {stored_count} out of {len(events)} events")
    return events_data

if __name__ == "__main__":
    store_events_to_db()
