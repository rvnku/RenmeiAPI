import os
import dotenv


dotenv.load_dotenv()


REDIRECT_URI = os.getenv('REDIRECT_URI', 'http://127.0.0.1:8000/auth/callback')
DATABASE_URL = os.getenv('DATABASE_URL', 'sqlite:///./tokens.db')
if not (CLIENT_ID := os.getenv('CLIENT_ID')):
    raise ValueError('CLIENT_ID must be set in environment')
if not (CLIENT_SECRET := os.getenv('CLIENT_SECRET')):
    raise ValueError('CLIENT_SECRET must be set in environment')
if not (API_KEY := os.getenv('API_KEY')):
    raise ValueError('API_KEY must be set in environment')
SCOPE = 'streaming'
