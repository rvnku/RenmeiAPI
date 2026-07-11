from spotipy.oauth2 import SpotifyOAuth
from app.config import CLIENT_ID, CLIENT_SECRET, REDIRECT_URI, SCOPE
import asyncio


async def run_sync(func, *args, **kwargs):
    loop = asyncio.get_event_loop()
    return await loop.run_in_executor(None, lambda: func(*args, **kwargs))


def get_spotify_oauth(state: str):
    return SpotifyOAuth(
        client_id=CLIENT_ID,
        client_secret=CLIENT_SECRET,
        redirect_uri=REDIRECT_URI,
        scope=SCOPE,
        state=state,
        show_dialog=True
    )
