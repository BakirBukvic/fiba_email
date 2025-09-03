#!/usr/bin/env python3
"""
FIBA 3x3 Events Scraper and Database Storage
Main runner script that fetches events and stores them in the database.
"""

import sys
import os

# Add the current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from get_events.store_db import store_events_to_db
from db.make_db import get_all_events, get_open_registrations

def main():
    """
    Main function that runs the complete scraping and storage process
    """
    print("=" * 50)
    print("FIBA 3x3 Events Scraper Starting...")
    print("=" * 50)
    
    try:
        # Run the scraping and storage process
        events_data = store_events_to_db()
        
        print("\n" + "=" * 50)
        print("Process completed successfully!")
        print("=" * 50)
        
        # Show summary from database
        all_events = get_all_events()
        open_events = get_open_registrations()
        
        print(f"\nDatabase Summary:")
        print(f"- Total events in database: {len(all_events)}")
        print(f"- Events with open registration: {len(open_events)}")
        
        if open_events:
            print(f"\nUpcoming events with open registration:")
            for event in open_events[:5]:  # Show first 5
                print(f"  • {event[1]} in {event[5]} - {event[3][:10]}")
        
        return True
        
    except Exception as e:
        print(f"\n❌ Error during scraping process: {e}")
        return False

if __name__ == "__main__":
    success = main()
    if success:
        print("\n✅ All done! Events have been scraped and stored in the database.")
    else:
        print("\n❌ Process failed. Check the error messages above.")
        sys.exit(1)
