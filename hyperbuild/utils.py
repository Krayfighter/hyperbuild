
import os
import typing
import tomllib


def check_valid_file(path: os.PathLike, extension_type = "*") -> bool:
    if not path.endswith("." + "extension_type") and extension_type != "*":
        raise RuntimeError("file type incorrect")
    
    if os.path.exists(path):
        # the path does exists
        if os.path.isfile(path):
            # the path leads to a file
            return True
        else:
            # the path is not a file
            return False
    else:
        # path does not exist
        return False


def parse(path: str) -> dict:
    if not check_valid_file(path):
        raise RuntimeError("parsing invalid file")
    
    parse_data: dict
    
    with open(path, "rb") as config_file:
        parse_data = tomllib.load(config_file)
    
    return parse_data
