import logging
import datetime
from logging.handlers import TimedRotatingFileHandler


class NodeLogger:
    def __init__(self, node_id):

        # Create a logger
        self.logger = logging.getLogger("nod" + node_id)
        self.logger.setLevel(logging.DEBUG)

        # Create console handler
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.DEBUG)

        # Create a TimedRotatingFileHandler
        current_date = datetime.datetime.now().strftime("%Y-%m-%d")
        log_file_name = f"node{node_id}_{current_date}.log"

        file_handler = TimedRotatingFileHandler(
            filename=log_file_name,  # Log file name
            when='midnight',  # Roll over at midnight
            interval=1,  # Create a new log file daily
            backupCount=30  # Keep up to 30 backup log files
        )
        file_handler.setLevel(logging.DEBUG)

        # Create formatter
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

        # Attach formatter to handlers
        console_handler.setFormatter(formatter)
        file_handler.setFormatter(formatter)

        # Add handlers to the logger
        self.logger.addHandler(console_handler)
        self.logger.addHandler(file_handler)

    def getLogger(self):
        return self.logger
