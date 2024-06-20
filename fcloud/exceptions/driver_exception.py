class DriverException(BaseException):
    def __init__(self, data_error: tuple) -> None:
        self.title, self.message = data_error


class DropboxException(DriverException):
    pass
