class Utils:

    @staticmethod
    def router_base_path_calculator(router_name: str):
        from .config_manager import ConfigManager

        BASE_PATH = ConfigManager.get_conf_value(
            config_file_name='api',
            section='api',
            value='base_path'
        )
        CURRENT_VERSION = ConfigManager.get_conf_value(
            config_file_name='api',
            section='api',
            value=f'current_version'
        )
        ROUTER_BASE_PATH = ConfigManager.get_conf_value(
            config_file_name='api',
            section='routers',
            value=f'{router_name}_router_base_path'
        )
        return f"{BASE_PATH}{CURRENT_VERSION}/{ROUTER_BASE_PATH}"