"""logger module to log the experiment data
    
"""

import logging


# Create a custom logger
logger = logging.getLogger("generate_data")
# Create handlers
f_handler = logging.FileHandler("util/logging/experiment.log", mode="a")
#f_handler.setLevel(logging.DEBUG)

# Create formatters and add it to handlers
f_format = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
f_handler.setFormatter(f_format)

# Add handlers to the logger
logger.addHandler(f_handler)
logger.setLevel(logging.DEBUG)


# Create a custom logger
inference_logger = logging.getLogger("inference")
# Create handlers
i_f_handler = logging.FileHandler("util/logging/inference.log", mode="a")
#i_f_handler.setLevel(logging.DEBUG)

# Create formatters and add it to handlers
i_f_format = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
i_f_handler.setFormatter(i_f_format)

# Add handlers to the logger
inference_logger.addHandler(i_f_handler)
inference_logger.setLevel(logging.DEBUG)    


# Create a custom logger
inference2_logger = logging.getLogger("inference2")
# Create handlers
i_f_handler = logging.FileHandler("util/logging/inference2.log", mode="a")
#i_f_handler.setLevel(logging.DEBUG)

# Create formatters and add it to handlers
i_f_format = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
i_f_handler.setFormatter(i_f_format)

# Add handlers to the logger
inference2_logger.addHandler(i_f_handler)
inference2_logger.setLevel(logging.DEBUG)    

# Create a custom logger
inference3_logger = logging.getLogger("inference3")
# Create handlers
i_f_handler = logging.FileHandler("util/logging/inference3.log", mode="a")
#i_f_handler.setLevel(logging.DEBUG)

# Create formatters and add it to handlers
i_f_format = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
i_f_handler.setFormatter(i_f_format)

# Add handlers to the logger
inference3_logger.addHandler(i_f_handler)
inference3_logger.setLevel(logging.DEBUG)    