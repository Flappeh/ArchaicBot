from dotenv import load_dotenv
import os 


load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHANNEL_WELCOME = int(os.getenv("CHANNEL_WELCOME"))
CHANNEL_LEAVE = int(os.getenv("CHANNEL_LEAVE"))