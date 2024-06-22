from ...exceptions.config_errors import ConfigError


class DropboxConfigError(ConfigError):
    app_key_empty_error = (
        "App key error",
        "The app_key field is empty. Set it in the configuration before getting the access token",
    )

    app_secret_error = (
        "App secret error",
        "Parsing error of app_secret field. It is possible that this field does not exist. The configuration file may be corrupted",
    )
