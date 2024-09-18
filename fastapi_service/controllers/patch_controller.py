from modules.base_controller import BaseController
from fastapi.response import JSONResponse

class PatchController(BaseController):
    
    def __init__(self) -> None:
        super().__init__()
        
    async def edit_book(to_edit: dict) -> JSONResponse:
        pass