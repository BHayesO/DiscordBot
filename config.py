from dotenv import load_dotenv
import os

load_dotenv()

API_KEY = os.getenv('API_KEY')
TWILIO_ACCOUNT_SID = os.getenv('TWILIO_ACCOUNT_SID')
TWILIO_AUTH_TOKEN = os.getenv('TWILIO_AUTH_TOKEN')
TWILIO_WHATSAPP_SANDBOX = 'whatsapp:+14155238886'
MY_WHATSAPP_NUMBER = os.getenv('MY_WHATSAPP_NUMBER')