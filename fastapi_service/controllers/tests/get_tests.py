import pytest
import asyncio
from unittest.mock import AsyncMock, patch
from get_controller import GetController

GetBookController = GetController()

@pytest.mark.asyncio
async def test_get_all_books_success():
    
    with patch('your_module.JWTSecurity.validate_jwt', return_value=True):
        db_mock = AsyncMock()
        db_mock.get_connection.return_value.cursor.return_value.fetchall.return_value = [('book1',), ('book2',)]
        
        service = GetBookController(db=db_mock)
        
        response = await service.get_all_books('valid_token')
        
        assert response.status_code == 200
        assert response.json() == {
            'STATUS': 'SUCCESS',
            'BOOKS': [('book1',), ('book2',)]
        }

@pytest.mark.asyncio
async def test_get_all_books_invalid_token():
    
    with patch('your_module.JWTSecurity.validate_jwt', return_value=False):
        db_mock = AsyncMock()
        service = GetBookController(db=db_mock)
        
        response = await service.get_all_books('invalid_token')
        
        assert response.status_code == 200
        assert response.json() == {'STATUS': 'FAILED'}
