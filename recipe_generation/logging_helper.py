import logging


def setup_logging(log_file_path, desired_logging_level=logging.WARNING):
    file_handler = logging.FileHandler(log_file_path)
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - [%(module)s] - %(message)s',
                                  datefmt='%Y-%m-%d %H:%M:%S')
    file_handler.setFormatter(formatter)
    file_handler.setLevel(desired_logging_level)
    logging.root.setLevel(desired_logging_level)
    logging.getLogger().addHandler(file_handler)
