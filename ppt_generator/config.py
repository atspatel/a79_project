from dotenv import load_dotenv
import os
# Load environment variables from the .env file
load_dotenv()

JWT_SIGNING_KEY = os.getenv('JWT_SIGNING_KEY')

OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
PEXEL_API_KEY = os.getenv('PEXEL_API_KEY')
