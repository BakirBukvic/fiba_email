def notify_new_events(new_events):
    """
    Simple notification for new events
    """
    if not new_events:
        return
    
    print("NEW EVENTS:")
    for event in new_events:
        registration = "OPEN" if event['registrationIsOpen'] else "CLOSED"
        print(f"{event['name']} - {event['city']} - {registration}")

def notify_missing_events(missing_events):
    """
    Simple notification for missing events
    """
    if not missing_events:
        return
    
    print("MISSING EVENTS:")
    for event in missing_events:
        registration = "OPEN" if event['registrationIsOpen'] else "CLOSED"
        print(f"{event['name']} - {event['city']} - {registration}")

def send_notifications(new_events, missing_events):
    """
    Send both types of notifications
    """
    if new_events:
        notify_new_events(new_events)
    
    if missing_events:
        notify_missing_events(missing_events)
