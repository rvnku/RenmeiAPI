from fastapi import APIRouter, HTTPException, Query, Depends
from fastapi.responses import RedirectResponse
from datetime import datetime, timedelta, timezone
from app.database import get_database
from app.utils import run_sync, get_spotify_oauth
from app.dependencies import validate_api_key
from aiosqlite import Connection


router = APIRouter(prefix='/auth', tags=['auth'])


@router.get('/login')
async def auth_login(user_id: str = Query(..., description='Discord user ID')):
    oauth = get_spotify_oauth(state=user_id)
    auth_url = oauth.get_authorize_url()
    return RedirectResponse(auth_url)

@router.get('/callback')
async def auth_callback(
    code: str = Query(...),
    state: str = Query(...),
    database: Connection = Depends(get_database)
):
    if not code or not state:
        raise HTTPException(status_code=400, detail='Missing code or state')

    oauth = get_spotify_oauth(state=state)
    try:
        token_info = await run_sync(oauth.get_access_token, code, as_dict=True)
    except Exception as exc:
        raise HTTPException(status_code=400, detail=f'Token exchange failed: {str(exc)}')

    if not token_info:
        raise HTTPException(status_code=400, detail='Invalid code')

    access_token = token_info['access_token']
    refresh_token = token_info.get('refresh_token')
    expires_in = token_info.get('expires_in', 3600)
    expires_at = datetime.now(timezone.utc) + timedelta(seconds=expires_in)

    await database.execute('''
        INSERT INTO users (user_id, access_token, refresh_token, expires_at)
        VALUES (?, ?, ?, ?)
        ON CONFLICT(user_id) DO UPDATE SET
            access_token = excluded.access_token,
            refresh_token = excluded.refresh_token,
            expires_at = excluded.expires_at
    ''', (state, access_token, refresh_token, expires_at.isoformat()))
    await database.commit()

    return {'message': 'Authorization successful! You can now close this page.'}

@router.get('/token')
async def get_token(
    user_id: str = Query(...),
    database: Connection = Depends(get_database),
    _: str = Depends(validate_api_key)
):
    async with database.execute(
        'SELECT access_token, refresh_token, expires_at FROM users WHERE user_id = ?',
        (user_id,)
    ) as cursor:
        row = await cursor.fetchone()

    if not row:
        raise HTTPException(status_code=404, detail='User not found. Please run /auth/login first.')

    access_token, refresh_token, expires_at_str = row
    expires_at = datetime.fromisoformat(expires_at_str)

    if expires_at < datetime.now(timezone.utc) + timedelta(seconds=60):
        if not refresh_token:
            raise HTTPException(status_code=401, detail='No refresh token. Re-authorize.')
    
        oauth = get_spotify_oauth(state=user_id)
        try:
            new_token_info = await run_sync(oauth.refresh_access_token, refresh_token)
        except Exception as e:
            raise HTTPException(status_code=400, detail=f'Refresh failed: {str(e)}')

        if not new_token_info:
            raise HTTPException(status_code=400, detail='Refresh token invalid. Re-authorize.')

        new_access_token = new_token_info['access_token']
        new_expires_in = new_token_info.get('expires_in', 3600)
        new_expires_at = datetime.now(timezone.utc) + timedelta(seconds=new_expires_in)

        await database.execute(
            'UPDATE users SET access_token = ?, expires_at = ? WHERE user_id = ?',
            (new_access_token, new_expires_at.isoformat(), user_id)
        )
        await database.commit()
        access_token = new_access_token

    return {'access_token': access_token}
