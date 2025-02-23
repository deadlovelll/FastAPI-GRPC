from rest_framework.views import APIView
from rest_framework.response import Response

from django_service.base.modules.logger.logger import LoggerModule

class BaseAPIView(APIView):
    
    """
    Base API view that provides a logger and standardized response creation.

    This class sets up a logger for each view (using the view’s class name)
    and provides a helper method to generate responses in a consistent format.
    
    Attributes:
        logger (logging.Logger): The logger instance for this view.
    """
    
    def __init__ (
        self, 
        **kwargs,
    ) -> None:
        
        """
        Initialize the BaseAPIView and set up the logger.

        Args:
            **kwargs: Additional keyword arguments passed to the parent APIView.
        """
        
        super().__init__(**kwargs)
        self.logger = LoggerModule()

    def create_response (
        self, 
        data: dict, 
        status_code: int = 200,
    ) -> Response:
        
        """
        Creates a standardized JSON response.

        Args:
            data (dict): The response data.
            status_code (int, optional): HTTP status code for the response. Defaults to 200.

        Returns:
            Response: A DRF Response object containing the provided data and status code.
        """
        
        return Response (
            data,
            status=status_code,
        )
