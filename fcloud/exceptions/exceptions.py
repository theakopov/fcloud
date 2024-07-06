class FcloudException(Exception):
    def __init__(self, title: str, message: str) -> None:
        self.title = title
        self.message = message


class FcloudConfigException(FcloudException):
    pass


class DriverException(FcloudException):
    pass
