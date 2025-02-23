import inspect
from abc import ABC, abstractmethod

from fastapi_service.decorators.jwt_ssecurity.jwt_security import JWTSecurity

class BaseRouter(ABC):
    
    def __init__ (
        self, 
        auto_protect: bool = False,
    ) -> None:
        
        """
        Initialize BaseRouter with optional auto-protection.
        
        Args:
            auto_protect (bool): If True, all methods are auto-decorated with JWT protection.
        """
        
        self.jwt_protector = JWTSecurity()
        if auto_protect:
            self._auto_decorate_methods()

    def _auto_decorate_methods (
        self,
    ) -> None:
        
        """
        Automatically decorates all instance methods with `jwt_required` if `auto_protect=True`.
        """
        
        for name, method in inspect.getmembers (
            self, 
            predicate=inspect.ismethod,
        ):
            if not name.startswith("_"):  # Skip private methods
                setattr (
                    self, 
                    name, 
                    self.jwt_protector.jwt_required(method),
                )

    @abstractmethod
    def _setup_routes(self):
        
        """Abstract method to be implemented by subclasses"""
        
        pass