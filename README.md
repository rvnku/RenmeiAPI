# Renmei API

```sh
uv pip install -r requirements.txt
uvicorn app.main:app \
  --host 0.0.0.0 \
  --port 443 \
  --ssl-certfile cert/fullchain.pem \
  --ssl-keyfile cert/privkey.pem
```
