import os
from textwrap import dedent

import yadisk

from ...exceptions.config_errors import ConfigError
from ...utils.config import edit_config
from ...utils.config import get_field


class Yandex:
    def __init__(self):
        self._conf = os.environ["FCLOUD_CONFIG_PATH"]
        title, message = ConfigError.field_error
        error = (title, message.format("client_id", self._conf))
        self._cient_id = get_field("client_id", error, section="YANDEX")

        error = (title, message.format("client_secret", self._conf))
        self._client_secret = get_field("client_secret", error, section="YANDEX")

        self._app = yadisk.Client(self._cient_id, self._client_secret)

    def get_token(self):
        """Generates a code that must be validated by clicking
        on the link to receive the token"""
        code_obj = self._app.get_device_code()
        input(
            dedent(
                f"""\
                Enter the code `{code_obj.user_code}` at this link {code_obj.verification_url}.
                After you enter the code, press any key.
                """
            )
        )
        token = self._app.get_token_from_device_code(code_obj.device_code)
        edit_config("YANDEX", "token", token.refresh_token)
