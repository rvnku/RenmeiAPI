from spotipy.oauth2 import SpotifyOAuth
from app.env import Env
import asyncio


async def run_sync(func, *args, **kwargs):
    loop = asyncio.get_event_loop()
    return await loop.run_in_executor(None, lambda: func(*args, **kwargs))


def get_spotify_oauth(state: str):
    return SpotifyOAuth(
        client_id=Env.client_id,
        client_secret=Env.client_secret,
        redirect_uri=Env.redirect_uri,
        scope='streaming',
        state=state,
        show_dialog=True
    )
