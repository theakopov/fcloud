from .base_error import FcloudError


class CFLError(FcloudError):
    cfl_error = (
        "CFLs can't be sent to the cloud",
        """This file is already in the cloud. Use "fcloud get" to download it""",
    )

    not_exists_cfl_error = (
        "CFL is not exists",
        "Unable to locate this cfl",
    )

    incorrect_cfl_error = ("Incorrect cfl", """A valid cfl starts with '%cfl:'""")

    near_with_folder_error = (
        "Unavailable to use --near with folders",
        """Currently, fcloud does not support the near option in relation to folders""",
    )
