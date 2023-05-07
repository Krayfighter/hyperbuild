# from ctypes import c_char

target_type = {
    "executable": 1,
    "static_library": 2,
    "dynamic_library": 3
}

# class defining a full project with possibly multiple different targets
class Project:
    pass

# outline for defining a compiler and how to call it
class Compiler:
    def __init__(self, name: str):
        name
    
    def compile(self):
        pass
    
    def link(self):
        pass
    
    def is_valid_flag(self, flag: str):
        pass
    
    compiler_path: str
    compiler_flags: list(str)
    is_unix_style_cli_args: bool

# create a target to compile
class CompileTarget:
    def __init__(self, target_name: str, compiler: Compiler):
        # self.target_name = target_name
        target_name
        compiler
        pass
    
    # add source files to the target
    def add_source_file(self, file_path: str):
        self.source_files.append(file_path)
    
    def add_source_files(self, file_paths: list(str)):
        self.source_files.append(file_paths)
    
    # add link directory to target
    def add_link_dir(self, dir_path: str):
        self.link_dirs.append(dir_path)
    
    def add_link_dirs(self, dir_paths: list(str)):
        self.link_dirs.append(dir_paths)
    
    # add included directories to the target 
    def add_include_dir(self, dir_path: str):
        self.include_dirs.append(dir_path)
    
    def add_include_dirs(self, dir_paths: list(str)):
        self.include_dirs.append(dir_paths)
    
    # aadd aa compiler flag manually
    def add_compiler_flag(self, flag: str):
        self.compiler_flags.append(flag)
    
    def add_compiler_flags(self, flags: list(str)):
        self.compiler_flags.append(flags)
    
    target_name: str
    source_files: list(str)
    include_dirs: list(str)
    link_dirs: list(str)
    compiler_flags: list(str)
    compiler: Compiler

if __name__ == '__main__':
    print('test')