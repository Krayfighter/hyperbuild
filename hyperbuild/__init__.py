
import os
import typing
import sys
import argparse

# import hyperbuild.parse_build as parse_build
import hyperbuild.target_types as target_types
import hyperbuild.utils as utils

def build_entry_point() -> None:
    os.system('clear')
    parser = argparse.ArgumentParser(
        prog="hyperbuild",
        description="good build system (hopefully)",
        epilog="insert not very useful help message here"
    )
    parser.add_argument('-r', '--run')
    args = parser.parse_args()
    
            
    # print(os.getcwd())
    # parse_build_file.parse("/home/aidenk/Desktop/hyperbuild/example/toolchain.toml")
    # build_dir = os.path.join(os.getcwd(), "example/toolchain.toml")
    build: dict = utils.parse("example/hyperbuild.toml")
    project = target_types.Project(build)
    # print(project)
    project.build()
    if args.run:
        # TODO change this to be dynamic, currently is a static dir
        os.system(project.targets['main']['builder'].build_dir + "/main")
    return