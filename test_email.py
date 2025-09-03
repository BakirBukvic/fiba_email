#!/usr/bin/env python3
"""
Test script for email notifications
"""

import sys
import os

# Add the parent directory to the path
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, parent_dir)

def test_email_setup():
    """Test if email configuration is properly set up"""
    print("🧪 TESTING EMAIL CONFIGURATION")
    print("=" * 40)
    
    try:
        from notify_events.notify import GMAIL_USER, GMAIL_APP_PASSWORD, RECIPIENTS
        
        print(f"Gmail User: {GMAIL_USER}")
        print(f"App Password: {'*' * len(GMAIL_APP_PASSWORD) if GMAIL_APP_PASSWORD and GMAIL_APP_PASSWORD != 'your-app-password' else 'NOT SET'}")
        print(f"Recipients: {RECIPIENTS}")
        
        if not GMAIL_USER or not GMAIL_APP_PASSWORD or not RECIPIENTS:
            print("\n❌ Email not configured!")
            print("1. Copy .env.example to .env")
            print("2. Update .env with your Gmail credentials")
            print("3. Generate Gmail App Password (see instructions in .env.example)")
            print("4. Install python-dotenv: pip install python-dotenv")
            return False
        
        print("\n✅ Email configuration looks good!")
        return True
        
    except Exception as e:
        print(f"❌ Error loading email config: {e}")
        print("Make sure .env file exists and python-dotenv is installed")
        return False

def send_test_email():
    """Send a test email"""
    if not test_email_setup():
        return
    
    print("\n📧 SENDING TEST EMAIL")
    print("=" * 30)
    
    from notify_events.notify import send_email
    
    subject = "FIBA 3x3 Test Email"
    body = """This is a test email from your FIBA 3x3 event monitoring system.

If you received this email, your configuration is working correctly!

Test Details:
- System: FIBA 3x3 Event Monitor
- Time: {time}
- Status: Email system operational

You can now run the main scraping system and receive notifications when events change.
""".format(time=datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    
    success = send_email(subject, body)
    
    if success:
        print("✅ Test email sent successfully!")
    else:
        print("❌ Failed to send test email")

def test_notification_system():
    """Test the notification system with fake data"""
    print("\n🔔 TESTING NOTIFICATION SYSTEM")
    print("=" * 35)
    
    from notify_events.notify import send_notifications
    
    # Create fake test data
    fake_new_events = [
        {
            'name': 'TEST: New Tournament Sarajevo',
            'city': 'Sarajevo',
            'registrationIsOpen': True,
            'startDate': '2025-12-01T00:00:00',
            'endDate': '2025-12-02T23:59:59'
        }
    ]
    
    fake_missing_events = [
        {
            'name': 'TEST: Cancelled Tournament Mostar',
            'city': 'Mostar',
            'registrationIsOpen': False,
            'startDate': '2025-11-15T00:00:00',
            'endDate': '2025-11-16T23:59:59'
        }
    ]
    
    print("Sending test notification with fake data...")
    send_notifications(fake_new_events, fake_missing_events)

def main():
    print("📧 EMAIL NOTIFICATION TESTER")
    print("=" * 35)
    print("Setup: Copy .env.example to .env and configure your Gmail settings")
    print()
    print("1. Test email configuration")
    print("2. Send test email")
    print("3. Test notification system")
    print()
    
    choice = input("Choose option (1-3): ").strip()
    
    if choice == "1":
        test_email_setup()
    elif choice == "2":
        send_test_email()
    elif choice == "3":
        test_notification_system()
    else:
        print("❌ Invalid choice")

if __name__ == "__main__":
    from datetime import datetime
    main()
