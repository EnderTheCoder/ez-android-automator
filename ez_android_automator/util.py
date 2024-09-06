import pathlib


def posix_path_join(*args):
    return str(pathlib.PurePosixPath(*args))

def remote_file_path_escape(path: str):
    return path.replace('(', '\\(').replace(')', '\\)')