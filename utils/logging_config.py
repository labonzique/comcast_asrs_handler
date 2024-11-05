import os
import logging

def setup_logging(log_level=logging.INFO):
    """
    Sets up logging configuration for the application.
    
    :param log_level: Logging level (default is logging.INFO)
    """
    log_directory = "logs"
    os.makedirs(log_directory, exist_ok=True)
    log_file_path = os.path.join(log_directory, "app.log")

    # Open the log file in write mode to clear it
    with open(log_file_path, "w"):
        pass  # This clears the content of the log file

    logging.basicConfig(
        level=log_level,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        handlers=[
            logging.StreamHandler(),
            logging.FileHandler(log_file_path, mode="a", encoding="utf-8")
        ]
    )
    logging.info("Logging is set up and log file cleared.")
