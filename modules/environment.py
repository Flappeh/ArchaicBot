from dotenv import load_dotenv
import os 


load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
WELCOME_CHANNEL_ID = os.getenv("WELCOME_CHANNEL_ID")
LEAVE_CHANNEL_ID = os.getenv("LEAVE_CHANNEL_ID")