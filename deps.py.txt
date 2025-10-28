import os, jwt
from fastapi import Header, HTTPException
from jwt import PyJWKClient
from dotenv import load_dotenv

load_dotenv()
JWKS_URL = os.getenv("SUPABASE_JWKS_URL")

def get_current_user(authorization: str = Header(...)):
    try:
        scheme, token = authorization.split()
        if scheme.lower() != "bearer":
            raise ValueError("Bad scheme")
        jwks = PyJWKClient(JWKS_URL)
        signing_key = jwks.get_signing_key_from_jwt(token).key
        payload = jwt.decode(
            token, signing_key, algorithms=["RS256"], audience=None, options={"verify_aud": False}
        )
        return {"sub": payload["sub"]}
    except Exception:
        raise HTTPException(status_code=401, detail="Invalid auth token")
