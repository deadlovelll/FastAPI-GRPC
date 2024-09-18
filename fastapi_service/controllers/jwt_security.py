import asyncio
import aiohttp

class JWTSecurity:
    
    @staticmethod
    async def validate_jwt(token: str) -> bool:
        
        validation_url = 'http://localhost:8000/api/validate-token/'
        
        async with aiohttp.ClientSession() as session:
            async with session.post(validation_url, json={'token':token}) as resp:
                response = await resp.json()
                
                return bool(response['valid'])
            