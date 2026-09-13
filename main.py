from fastapi import FastAPI, Request
from fastapi.responses import PlainTextResponse
from nacl.public import PrivateKey, PublicKey

PRIVATE_KEY = PrivateKey.generate()
user_keys: dict[str, PublicKey] = {}

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get(
    "/api/server_key",
    summary="The server's public key",
    response_class=PlainTextResponse,
)
async def server_key():
    return bytes(PRIVATE_KEY.public_key)


@app.post(
    "/api/user_key",
    summary="Set the public key associated with the poster's IP address",
)
async def user_key(request: Request):
    key = await request.body()
    client = request.client
    if not client:
        raise UserWarning("`client` is none")
    else:
        user_keys[client.host] = PublicKey(key)
