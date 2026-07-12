from abc import ABC
import dotenv, os


dotenv.load_dotenv()


class Env(ABC):
    redirect_uri = os.getenv('REDIRECT_URI', 'http://127.0.0.1:8000/auth/callback')
    database_url = os.getenv('DATABASE_URL', 'sqlite:///./tokens.db')
    if not (client_id := os.getenv('CLIENT_ID', '')):
        raise ValueError('CLIENT_ID must be set in environment')
    if not (client_secret := os.getenv('CLIENT_SECRET', '')):
        raise ValueError('CLIENT_SECRET must be set in environment')
    if not (api_key := os.getenv('API_KEY', '')):
        raise ValueError('API_KEY must be set in environment')
    host = os.getenv('HOST', '127.0.0.1')
    port = int(os.getenv('PORT', 8081))
    ssl_sertfile = os.getenv('SSL_SERTFILE')
    ssl_keyfile = os.getenv('SSL_KEYFILE')
