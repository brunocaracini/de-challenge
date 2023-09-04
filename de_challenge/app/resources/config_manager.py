import os
import ast
import json
import configparser
from pathlib import Path


class ConfigManager:
    """A utility class to manage configuration files."""

    BASE_PATH = Path(__file__).resolve().parent.parent

    @classmethod
    def get_conf_value(
        cls,
        config_file_name: str,
        section: str,
        value: str,
        variable_type: str = "string",
    ):
        """
        Retrieves the value of a configuration parameter from the specified
        configuration file. The value can be of type 'string', 'integer',
        'float', 'boolean', or 'dict' (JSON). The default variable_type is
        'string'.

        Args:
            config_file_name (str): The name of the configuration file (without
            the '.conf' extension).
            section (str): The name of the section in the configuration file
            where the parameter is defined.
            value (str): The name of the parameter whose value is to be
            retrieved.
            variable_type (str, optional): The type of the parameter value.
            Defaults to 'string'.

        Returns:
            Any: The value of the specified parameter. The value is of the type
            specified by the variable_type argument.
        """

        config_parser = configparser.RawConfigParser()
        config_file_path = str(
            os.path.join(cls.BASE_PATH, "config", f"{config_file_name.lower()}.conf")
        )
        config_parser.read(config_file_path)

        if variable_type == "str" or variable_type == "string":
            value = config_parser.get(section.upper(), value.upper())
        elif variable_type == "list" or variable_type == "array":
            value = config_parser.get(section.upper(), value.upper())
            value = ast.literal_eval(value)
        elif variable_type == "int" or variable_type == "integer":
            value = config_parser.getint(section.upper(), value.upper())
        elif variable_type == "float" or variable_type == "real":
            value = config_parser.getfloat(section.upper(), value.upper())
        elif variable_type == "bool" or variable_type == "boolean":
            value = config_parser.getboolean(section.upper(), value.upper())
        elif variable_type == "json" or variable_type == "dict":
            value = config_parser.get(section.upper(), value.upper())
            value = json.loads(value)
        return value