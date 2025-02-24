from grpc_service.modules.logger.logger import LoggerModule

class BaseGRPCController:
    
    """
    A base gRPC controller to standardize response handling, error management,
    and logging across all gRPC services.
    """

    def __init__ (
        self,
        logger: LoggerModule = LoggerModule(),
    ) -> None:
        
        """Initialize logger."""
        
        self.logger = logger.logger_initialization()

    def success_response (
        self, 
        response,
    ):
        
        """
        Returns a successful gRPC response.

        Args:
            response: The response message.

        Returns:
            gRPC response object.
        """
        
        self.logger.info('Response sent successfully.')
        return response

    def error_response (
        self, 
        context, 
        code, 
        message: str,
    ) -> None:
        
        """
        Handles gRPC errors by setting context and returning an empty response.

        Args:
            context: gRPC context object.
            code: gRPC status code (grpc.StatusCode).
            message (str): Error message.

        Returns:
            An empty response with the error details set in the context.
        """
        
        self.logger.error(f'Error {code}: {message}')
        context.set_code(code)
        context.set_details(message)
        return None  # Return empty response
