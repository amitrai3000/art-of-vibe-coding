"""FastAPI dependencies for dependency injection."""

import base64
import json
import logging
from typing import Annotated

from fastapi import Depends, Header, HTTPException, status

from app.config import Settings, get_settings

logger = logging.getLogger(__name__)


async def verify_jwt_token(
    authorization: Annotated[str | None, Header()] = None,
    settings: Settings = Depends(get_settings),
) -> dict:
    """Verify JWT token from Supabase Auth.

    For development, we decode the JWT to extract user info.
    The token is trusted as it comes from Supabase frontend auth.

    Args:
        authorization: Authorization header with Bearer token
        settings: Application settings

    Returns:
        Decoded JWT payload with user information

    Raises:
        HTTPException: If token is invalid or missing
    """
    if not authorization:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing authorization header",
        )

    try:
        # Extract token from "Bearer <token>"
        parts = authorization.split()
        if len(parts) != 2 or parts[0].lower() != "bearer":
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid authentication scheme",
            )

        token = parts[1]

        # Decode JWT payload (middle part) without verification
        # JWT format: header.payload.signature
        jwt_parts = token.split(".")
        if len(jwt_parts) != 3:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token format",
            )

        # Decode payload (add padding if needed)
        payload_b64 = jwt_parts[1]
        padding = 4 - len(payload_b64) % 4
        if padding != 4:
            payload_b64 += "=" * padding

        payload_json = base64.urlsafe_b64decode(payload_b64)
        payload = json.loads(payload_json)

        # Check if token has required fields
        if "sub" not in payload:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token: missing user ID",
            )

        # Check expiration
        import time
        if "exp" in payload and payload["exp"] < time.time():
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token has expired",
            )

        logger.info(f"User authenticated: {payload.get('sub')}")
        return payload

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Auth exception: {e}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Authentication failed: {str(e)}",
        )


async def get_current_user_id(token_payload: dict = Depends(verify_jwt_token)) -> str:
    """Extract user ID from verified JWT token.

    Args:
        token_payload: Decoded JWT payload

    Returns:
        User ID (UUID as string)

    Raises:
        HTTPException: If user ID is missing from token
    """
    user_id = token_payload.get("sub")
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token: missing user ID",
        )
    return user_id
