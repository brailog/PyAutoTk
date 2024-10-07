import os


class _ConfigLoader:
    """
    Configuration loader that checks environment variables for framework-wide settings.
    If a variable is not set, it falls back to a default value.
    """

    def __init__(self):
        """
        Initializes the configuration loader with environment variables or default values.
        """
        self.log_level = os.getenv("PYAUTOTK_LOG_LEVEL", "INFO")
        self.browser_type = os.getenv("PYAUTOTK_BROWSER_TYPE", "firefox")
        self.maximize_browser = os.getenv("PYAUTOTK_MAXIMIZE_BROWSER", "False").lower() == "true"
        self.headless_mode = os.getenv("PYAUTOTK_HEADLESS_MODE", "False").lower() == "true"
        self.artifacts_path = os.getenv("PYAUTOTK_ARTIFACTS_PATH", "./logs")

    def __repr__(self):
        """
        Returns a string representation of the current configuration.
        """
        return (
            f"ConfigLoader(log_level='{self.log_level}', browser_type='{self.browser_type}', "
            f"maximize_browser={self.maximize_browser}, headless_mode={self.headless_mode}, "
            f"artifacts_path='{self.artifacts_path}')"
        )


config = _ConfigLoader()
