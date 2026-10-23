from fastapi import Header, HTTPException

API_KEY = "ra_7Kx92mLpQwZf4Nn8TyH3RsBc"  # match your frontend header


def validate_api_key(x_api_key: str = Header(...)):
    if x_api_key != API_KEY:
        raise HTTPException(status_code=401, detail="Invalid API key")
    return x_api_key
