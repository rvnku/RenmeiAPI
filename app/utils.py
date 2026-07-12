from spotipy.oauth2 import SpotifyOAuth
from app.env import Env
import asyncio


def get_redirect_uri() -> str:
    proto = 'https' if Env.ssl_keyfile and Env.ssl_sertfile else 'http'
    return f'{proto}://{Env.host}:{Env.port}/auth/callback'


async def run_sync(func, *args, **kwargs):
    loop = asyncio.get_event_loop()
    return await loop.run_in_executor(None, lambda: func(*args, **kwargs))


def get_spotify_oauth(state: str):
    return SpotifyOAuth(
        client_id=Env.client_id,
        client_secret=Env.client_secret,
        redirect_uri=get_redirect_uri(),
        scope='streaming',
        state=state,
        show_dialog=True
    )
