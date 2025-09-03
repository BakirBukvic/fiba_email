#!/usr/bin/env python3
"""
Test script to verify new event detection functionality
Simulates adding new events to test the notification system
"""

import sys
import os
from datetime import datetime

# Add the parent directory to the path
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, parent_dir)

from db.make_db import insert_event, get_existing_event_ids, get_all_events

def create_test_event(event_id, name, city, start_date, end_date, registration_open=True):
    """Create a test event record"""
    return {
        'id': event_id,
        'name': name,
        'registrationIsOpen': registration_open,
        'startDate': start_date,
        'endDate': end_date,
        'city': city,
        'date_scraped': datetime.now().strftime("%Y-%m-%d")
    }

def add_test_events():
    """Add some fake test events to simulate new events being found"""
    
    print("🧪 ADDING TEST EVENTS TO SIMULATE NEW EVENTS")
    print("=" * 50)
    
    # Check current state
    existing_ids = get_existing_event_ids()
    print(f"Current events in database: {len(existing_ids)}")
    
    # Create some test events with unique IDs
    test_events = [
        create_test_event(
            "test-001-sarajevo-2025",
            "TEST EVENT: Sarajevo 3x3 Championship 2025", 
            "Sarajevo",
            "2025-10-15T00:00:00",
            "2025-10-16T23:59:59"
        ),
        create_test_event(
            "test-002-mostar-2025", 
            "TEST EVENT: Mostar Street Basketball",
            "Mostar",
            "2025-11-01T00:00:00", 
            "2025-11-02T23:59:59"
        ),
        create_test_event(
            "test-003-tuzla-2026",
            "TEST EVENT: Tuzla Winter Cup 2026",
            "Tuzla", 
            "2026-02-10T00:00:00",
            "2026-02-11T23:59:59",
            registration_open=False
        )
    ]
    
    # Add test events to database
    added_count = 0
    for event in test_events:
        if event['id'] not in existing_ids:
            insert_event(event)
            added_count += 1
            reg_status = "🟢 OPEN" if event['registrationIsOpen'] else "🔴 CLOSED"
            print(f"✅ Added: {event['name']} in {event['city']} - {reg_status}")
        else:
            print(f"⚠️  Skipped: {event['name']} (already exists)")
    
    print(f"\n📊 Added {added_count} test events to database")
    print(f"💡 Now run 'python run.py' to see if it detects these as 'new' events")
    print(f"   (It should NOT detect them as new since they're already in the database)")
    
    return added_count

def simulate_api_with_new_events():
    """
    Simulate what would happen if the API returned new events
    by temporarily modifying get_events function behavior
    """
    print("\n🎭 SIMULATING API RESPONSE WITH NEW EVENTS")
    print("=" * 50)
    
    # This simulates what the API might return with new events
    simulated_api_response = {
        "results": [
            # Existing events (these should already be in DB)
            {
                "id": "2ee22e60-c68b-459a-98f3-8c00cb11472d",
                "name": "3X3 SC BORIK 2025",
                "registrationIsOpen": True,
                "startDate": "2025-09-06T00:00:00",
                "endDate": "2025-09-07T23:59:59",
                "city": "Banja Luka"
            },
            # NEW simulated events (these should be detected as new)
            {
                "id": "simulated-new-001",
                "name": "SIMULATED: New Tournament Zenica", 
                "registrationIsOpen": True,
                "startDate": "2025-12-01T00:00:00",
                "endDate": "2025-12-02T23:59:59",
                "city": "Zenica"
            },
            {
                "id": "simulated-new-002",
                "name": "SIMULATED: Bihac Basketball Festival",
                "registrationIsOpen": False, 
                "startDate": "2026-03-15T00:00:00",
                "endDate": "2026-03-16T23:59:59", 
                "city": "Bihac"
            }
        ],
        "totalCount": 3,
        "currentPageNum": 1
    }
    
    # Save this to a JSON file that we can use for testing
    import json
    test_file = os.path.join(parent_dir, 'test_api_response.json')
    with open(test_file, 'w') as f:
        json.dump(simulated_api_response, f, indent=2)
    
    print(f"📝 Created simulated API response file: {test_file}")
    print(f"📋 Contains {len(simulated_api_response['results'])} events:")
    
    for event in simulated_api_response['results']:
        status = "🟢 OPEN" if event['registrationIsOpen'] else "🔴 CLOSED"
        print(f"   • {event['name']} in {event['city']} - {status}")
    
    print(f"\n💡 To test with this simulated data:")
    print(f"   1. Modify get_events.py to read from this JSON file instead of API")
    print(f"   2. Or use the test_with_simulated_data() function below")

def test_with_simulated_data():
    """Test the store_db functionality with simulated data"""
    print("\n🚀 TESTING WITH SIMULATED DATA")
    print("=" * 50)
    
    # Import the store_db function components
    from get_events.store_db import store_events_to_db
    from db.make_db import get_existing_event_ids
    
    # Get current state
    existing_ids = get_existing_event_ids()
    print(f"Events in database before test: {len(existing_ids)}")
    
    # Create a mock get_events function
    def mock_get_events():
        return {
            "results": [
                # One existing event (should not be flagged as new)
                {
                    "id": "2ee22e60-c68b-459a-98f3-8c00cb11472d",
                    "name": "3X3 SC BORIK 2025",
                    "registrationIsOpen": True,
                    "startDate": "2025-09-06T00:00:00",
                    "endDate": "2025-09-07T23:59:59",
                    "city": "Banja Luka"
                },
                # Two NEW events (should be flagged as new)
                {
                    "id": "mock-new-001",
                    "name": "MOCK: Completely New Tournament",
                    "registrationIsOpen": True,
                    "startDate": "2025-12-20T00:00:00",
                    "endDate": "2025-12-21T23:59:59",
                    "city": "Prijedor"
                },
                {
                    "id": "mock-new-002", 
                    "name": "MOCK: Another Fresh Event",
                    "registrationIsOpen": False,
                    "startDate": "2026-04-10T00:00:00",
                    "endDate": "2026-04-11T23:59:59",
                    "city": "Doboj"
                }
            ]
        }
    
    # Temporarily replace the get_events function
    import get_events.store_db as store_module
    original_get_events = store_module.get_events
    store_module.get_events = mock_get_events
    
    try:
        print("🔄 Running store_events_to_db with mocked data...")
        store_events_to_db()
    finally:
        # Restore original function
        store_module.get_events = original_get_events
    
    print("\n✅ Test completed!")

def cleanup_test_data():
    """Remove test events from database"""
    print("\n🧹 CLEANING UP TEST DATA")
    print("=" * 50)
    
    import sqlite3
    from db.make_db import get_db_connection
    
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Remove events with test IDs
    test_prefixes = ['test-', 'simulated-', 'mock-']
    
    removed_count = 0
    for prefix in test_prefixes:
        cursor.execute("DELETE FROM events WHERE id LIKE ?", (f"{prefix}%",))
        removed_count += cursor.rowcount
    
    conn.commit()
    conn.close()
    
    print(f"🗑️  Removed {removed_count} test events from database")
    
    # Also remove test file
    test_file = os.path.join(parent_dir, 'test_api_response.json')
    if os.path.exists(test_file):
        os.remove(test_file)
        print(f"🗑️  Removed test file: {test_file}")

def main():
    """Main test menu"""
    print("🧪 NEW EVENT DETECTION TESTER")
    print("=" * 40)
    print("1. Add test events to database")
    print("2. Create simulated API response")  
    print("3. Test with simulated data (RECOMMENDED)")
    print("4. Cleanup test data")
    print("5. Show current database state")
    print()
    
    choice = input("Choose option (1-5): ").strip()
    
    if choice == "1":
        add_test_events()
    elif choice == "2":
        simulate_api_with_new_events()
    elif choice == "3":
        test_with_simulated_data()
    elif choice == "4":
        cleanup_test_data()
    elif choice == "5":
        all_events = get_all_events()
        print(f"\n📊 Current database state ({len(all_events)} events):")
        for event in all_events:
            reg_status = "🟢 OPEN" if event[2] else "🔴 CLOSED"
            print(f"   • {event[1]} in {event[5]} - {reg_status} (ID: {event[0][:20]}...)")
    else:
        print("❌ Invalid choice")

if __name__ == "__main__":
    main()
