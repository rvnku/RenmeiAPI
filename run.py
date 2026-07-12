from app.env import Env
from app import app
import uvicorn


if __name__ == '__main__':
    uvicorn.run(
        app,
        host=Env.host,
        port=Env.port,
        ssl_certfile=Env.ssl_sertfile,
        ssl_keyfile=Env.ssl_keyfile,
        log_level='info'
    )
