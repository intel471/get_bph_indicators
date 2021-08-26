import os.path
from pathlib import Path
from datetime import datetime
import logging
import configparser


class GetBPHIndicatorsConfig:
    def __init__(self):
        self.script_path = os.path.dirname(os.path.realpath(__file__))
        self.config = None
        self.logger = None
        self.handler_console = None
        self.formatter_console = None
        self.handler_file = None
        self.formatter_file = None
        self.files_config_directory = ""
        self.files_log_directory = ""
        self.files_log_prefix = ""
        self.files_output_directory = ""
        self.files_output_file_json = ""
        self.titan_username = ""
        self.titan_api_key = ""
        self.titan_api_base_url = ""
        self.titan_api_batch_size = 100
        self.titan_user_agent = ""
        self.bph_tracking_tag = ""

    def initialise(self) -> bool:
        try:
            self.config = configparser.ConfigParser()
            self.config.read(os.path.join(self.script_path, "config", "get_bph_indicators.ini"))

            self.files_config_directory = self.config.get("files", "config_directory")
            self.files_log_directory = self.config.get("files", "log_directory")
            self.files_log_prefix = self.config.get("files", "log_prefix")
            self.files_output_directory = self.config.get("files", "output_directory")
            self.files_output_file_json = self.config.get("files", "output_file_json")

            self.logger = logging.getLogger("get_bph_indicators")
            self.logger.setLevel(logging.INFO)

            # Create a logging console handler and set the level to INFO.
            self.handler_console = logging.StreamHandler()
            self.handler_console.setLevel(logging.INFO)
            self.formatter_console = logging.Formatter("%(asctime)-15s - %(name)s - %(levelname)-8s - %(message)s")
            self.handler_console.setFormatter(self.formatter_console)
            self.logger.addHandler(self.handler_console)

            # Create a logging file handler and set the level to INFO.
            fn = os.path.join(self.script_path, self.files_log_directory, f"{self.files_log_prefix}{datetime.now().strftime('%Y-%m-%d_%H.%M.%S')}.log")
            self.handler_file = logging.FileHandler(fn, "w", encoding=None, delay=True)
            self.handler_file.setLevel(logging.INFO)
            self.formatter_file = logging.Formatter("%(asctime)-15s - %(name)s - %(levelname)-8s - %(message)s")
            self.handler_file.setFormatter(self.formatter_file)
            self.logger.addHandler(self.handler_file)

            self.titan_username = self.config.get("intel471", "titan_username")
            self.titan_api_key = self.config.get("intel471", "titan_api_key")
            self.titan_api_base_url = self.config.get("intel471", "titan_api_base_url")
            self.titan_api_batch_size = self.config.getint("intel471", "titan_api_batch_size")
            self.titan_user_agent = self.config.get("intel471", "titan_user_agent")
            self.bph_tracking_tag = self.config.get("intel471", "bph_tracking_tag")

            Path(self.files_log_directory).mkdir(parents=True, exist_ok=True)
            Path(self.files_output_directory).mkdir(parents=True, exist_ok=True)

        except Exception:
            print("Unable to initialise configuration.")
            return False
        else:
            return True
