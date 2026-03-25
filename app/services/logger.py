# Logging logic seperate from business logic

import logging
import sys

# Create a custom logger
logger = logging.getLogger("text2flow")
logger.setLevel(logging.INFO)

# Create handlers
c_handler = logging.StreamHandler(sys.stdout) # Logs to terminal
f_handler = logging.FileHandler("app.log")     # Logs to file named app.log

# Create formatters and add it to handlers
# Format: Time - Name - Level - Message
format = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
c_handler.setFormatter(format)
f_handler.setFormatter(format)

# Add handlers to the logger
logger.addHandler(c_handler)
logger.addHandler(f_handler)