import pathlib


def posix_path_join(*args):
    return str(pathlib.PurePosixPath(*args))
