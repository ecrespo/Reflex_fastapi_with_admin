from loguru import logger
import sys


# Define a singleton class for the logger
class LoggerSingleton:
    # Initialize the instance attribute
    _instance = None

    # Define the __new__ method
    def __new__(cls):
        # If an instance does not exist
        if cls._instance is None:
            # Remove any existing handlers
            logger.remove()
            # Add a new handler with custom settings
            logger.add(sys.stdout, colorize=True, format="<green>{time:HH:mm:ss}</green> | {level} | <level>{message}</level>")
            # Assign the logger instance to the _instance attribute
            cls._instance = logger
        # Return the instance
        return cls._instance


# Create a logger instance
logger = LoggerSingleton()