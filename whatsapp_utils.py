import requests
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Twilio credentials and WhatsApp sandbox configuration
TWILIO_ACCOUNT_SID = os.getenv('TWILIO_ACCOUNT_SID')
TWILIO_AUTH_TOKEN = os.getenv('TWILIO_AUTH_TOKEN')
TWILIO_WHATSAPP_SANDBOX = 'whatsapp:+14155238886'  # Twilio sandbox number
MY_WHATSAPP_NUMBER = os.getenv('MY_WHATSAPP_NUMBER')  # Your WhatsApp number

def send_whatsapp_message(body: str, media_url: str = None) -> bool:
    """
    Send a WhatsApp message via Twilio's API.
    
    :param body: The text message to send.
    :param media_url: (Optional) A URL for a media file to include in the message.
    :return: True if the message was sent successfully, False otherwise.
    """
    url = f"https://api.twilio.com/2010-04-01/Accounts/{TWILIO_ACCOUNT_SID}/Messages.json"
    data = {
        'From': TWILIO_WHATSAPP_SANDBOX,
        'To': MY_WHATSAPP_NUMBER,
        'Body': body,
    }
    if media_url:
        data['MediaUrl'] = media_url

    response = requests.post(url, data=data, auth=(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN))
    if response.status_code == 201:
        print("✅ WhatsApp message sent successfully!")
        return True
    else:
        print(f"❌ Failed to send WhatsApp message: {response.status_code} - {response.text}")
        return False
