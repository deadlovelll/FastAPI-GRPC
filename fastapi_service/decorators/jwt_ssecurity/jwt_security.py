import os
import aiohttp
from functools import wraps
from typing import Callable

class JWTSecurity:
    
    """
    A security utility for validating JWTs using an external API.
    """
    
    def __init__ (
        self,
    ) -> None:
        
        """
        Initializes JWTSecurity with a validation URL.
        """
        
        self.validation_url = os.getenv('JWT_VALIDATION_URL')

    async def validate_jwt (
        self,
        token: str,
    ) -> bool:
        
        """
        Asynchronously validates a JWT token via an external validation service.

        :param token: The JWT token to validate.
        :return: True if the token is valid, otherwise False.
        """
        
        async with aiohttp.ClientSession() as session:
            async with session.post (
                self.validation_url, 
                json={'token': token}
            ) as resp:
                
                response = await resp.json()
                return bool(response.get('valid', False))

    def jwt_required (
        self,
        func: Callable,
    ) -> Callable:
        
        """
        A decorator that ensures a valid JWT token is provided.

        :param func: The async function to wrap.
        :return: The wrapped function with JWT validation.
        """
        
        @wraps(func)
        async def wrapper (
            *args, 
            **kwargs,
        ):
            token = kwargs.get("token") or (args[0] if args else None)
            if not token:
                raise ValueError("JWT token is required.")

            is_valid = await JWTSecurity.validate_jwt(token)
            if not is_valid:
                raise PermissionError("Invalid JWT token.")

            return await func(*args, **kwargs)

        return wrapper
