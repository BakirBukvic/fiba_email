import smtplib
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime

# Load environment variables
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    print("python-dotenv not installed. Install with: pip install python-dotenv")

# Email configuration from .env file
GMAIL_USER = os.getenv('GMAIL_USER')
GMAIL_APP_PASSWORD = os.getenv('GMAIL_APP_PASSWORD')
RECIPIENTS = os.getenv('EMAIL_RECIPIENTS', '').split(',') if os.getenv('EMAIL_RECIPIENTS') else []

# Remove empty strings from recipients list
RECIPIENTS = [email.strip() for email in RECIPIENTS if email.strip()]

if not GMAIL_USER or not GMAIL_APP_PASSWORD or not RECIPIENTS:
    print("⚠️  Email configuration missing from .env file")
    print("Required variables: GMAIL_USER, GMAIL_APP_PASSWORD, EMAIL_RECIPIENTS")

def format_event_list(events, title):
    """Format a list of events for email"""
    if not events:
        return ""
    
    formatted = f"\n{title}:\n" + "="*50 + "\n"
    for event in events:
        registration = "OPEN" if event['registrationIsOpen'] else "CLOSED"
        start_date = event['startDate'][:10] if 'startDate' in event else 'N/A'
        end_date = event['endDate'][:10] if 'endDate' in event else 'N/A'
        formatted += f"• {event['name']}\n"
        formatted += f"  City: {event['city']}\n"
        formatted += f"  Registration: {registration}\n"
        formatted += f"  Dates: {start_date} to {end_date}\n\n"
    
    return formatted

def get_all_current_events():
    """Get all events currently in the database"""
    import sys
    import os
    parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    sys.path.insert(0, parent_dir)
    
    from db.make_db import get_all_events
    
    events = get_all_events()
    formatted_events = []
    
    for event in events:
        formatted_events.append({
            'id': event[0],
            'name': event[1],
            'registrationIsOpen': event[2],
            'startDate': event[3],
            'endDate': event[4],
            'city': event[5],
            'date_scraped': event[6] if len(event) > 6 else 'N/A'
        })
    
    return formatted_events

def create_email_content(new_events, missing_events):
    """Create the full email content"""
    subject = "FIBA 3x3 Events Update"
    
    # Email body
    body = f"FIBA 3x3 Events Update - {datetime.now().strftime('%Y-%m-%d %H:%M')}\n"
    body += "="*60 + "\n\n"
    
    # Add new events section
    if new_events:
        body += format_event_list(new_events, "NEW EVENTS DETECTED")
    
    # Add missing events section  
    if missing_events:
        body += format_event_list(missing_events, "EVENTS REMOVED/CANCELLED")
    
    # Always include all current events
    all_events = get_all_current_events()
    body += format_event_list(all_events, "ALL CURRENT EVENTS")
    
    body += f"\nUpdate completed at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
    
    return subject, body

def send_email(subject, body):
    """Send email via Gmail"""
    try:
        # Create message
        msg = MIMEMultipart()
        msg['From'] = GMAIL_USER
        msg['To'] = ', '.join(RECIPIENTS)
        msg['Subject'] = subject
        
        # Add body to email
        msg.attach(MIMEText(body, 'plain'))
        
        # Gmail SMTP configuration
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()  # Enable encryption
        server.login(GMAIL_USER, GMAIL_APP_PASSWORD)
        
        # Send email
        text = msg.as_string()
        server.sendmail(GMAIL_USER, RECIPIENTS, text)
        server.quit()
        
        print(f"Email sent successfully to: {', '.join(RECIPIENTS)}")
        return True
        
    except Exception as e:
        print(f"Failed to send email: {e}")
        return False

def notify_new_events(new_events):
    """
    Simple console notification for new events
    """
    if not new_events:
        return
    
    print("NEW EVENTS:")
    for event in new_events:
        registration = "OPEN" if event['registrationIsOpen'] else "CLOSED"
        print(f"{event['name']} - {event['city']} - {registration}")

def notify_missing_events(missing_events):
    """
    Simple console notification for missing events
    """
    if not missing_events:
        return
    
    print("MISSING EVENTS:")
    for event in missing_events:
        registration = "OPEN" if event['registrationIsOpen'] else "CLOSED"
        print(f"{event['name']} - {event['city']} - {registration}")

def send_notifications(new_events, missing_events):
    """
    Send both console and email notifications
    """
    # Console notifications (always)
    if new_events:
        notify_new_events(new_events)
    
    if missing_events:
        notify_missing_events(missing_events)
    
    # Email notifications (only if there are changes)
    if new_events or missing_events:
        subject, body = create_email_content(new_events, missing_events)
        send_email(subject, body)
