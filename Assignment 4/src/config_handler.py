import yaml

class ConfigHandler:

    """
    Config file handler
    """

    def read_config(self, config_filepath):
        """
        Read yaml file from directory and return as dict
        """
        with open(config_filepath, "r") as f_in:
            return yaml.safe_load(f_in)
