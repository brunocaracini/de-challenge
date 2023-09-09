class Utils:
    @staticmethod
    def router_base_path_calculator(router_name: str):
        from .config_manager import ConfigManager

        BASE_PATH = ConfigManager.get_conf_value(
            config_file_name="api", section="api", value="base_path"
        )
        CURRENT_VERSION = ConfigManager.get_conf_value(
            config_file_name="api", section="api", value=f"current_version"
        )
        ROUTER_BASE_PATH = ConfigManager.get_conf_value(
            config_file_name="api",
            section="routers",
            value=f"{router_name}_router_base_path",
        )
        return f"{BASE_PATH}{CURRENT_VERSION}/{ROUTER_BASE_PATH}".rstrip('/')

    @staticmethod
    def get_class_variables_from_object(obj: object):
        return [
            var
            for var in vars(obj)
            if not callable(getattr(obj, var))
            and not var.startswith("__")
            and var != "_sa_class_manager"
        ]
