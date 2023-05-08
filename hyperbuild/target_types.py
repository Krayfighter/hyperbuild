# from ctypes import c_char
import os

# import hyperbuild.toolchains as toolchains

target_type = {
    "executable": 1,
    "static_library": 2,
    "dynamic_library": 3
}

# class defining a full project with possibly multiple different targets
class Project:
    def __init__(self, config: dict):
        self.name = config['project']['name']
        # self.binary_dir = os.path.join(os.getcwd(), config['project']['binary_dir'])
        self.set_binary_dir(config['project']['binary_dir'])
        self.add_target(config['target'])
    
    def set_binary_dir(self, path: str):
        if not os.path.isdir(path):
            os.system('mkdir ' + path)
            # raise RuntimeError("binary does not exists for project")
        self.binary_dir = path
    
    # def add_target(target, dependencies = []):
    #     pass
    
    def build(self):
        self.target_tree['main']['builder'].build()
    
    def add_target(self, target_config: dict):
    
        build_target = None
        
        # handle build tree integration
        if target_config['name'] == None:
            print("no name founr")
            raise RuntimeError()
        else:
            # create the outline of the target in the tree
            self.target_tree[target_config['name']] = {
                "type": target_config['type'],
                "deps": target_config['deps'],
                "builder": None
            }
            build_target = BuildTarget(target_config['name'], gcc_compiler_command)
        
        # search the keys in the target config
        for (key, value) in target_config.items():
            match key:
                case "name":
                    pass
                case "type":
                    pass
                case "deps":
                    pass
                    # build_target.set_target_name(value)
                # case "toolchain":
                #     raise NotImplementedError
                case "build_dir":
                    build_target.set_build_dir(self.binary_dir + value)
                case "src_files":
                    build_target.add_source_files(value)
                case "include_dirs":
                    build_target.add_include_dirs(value)
                case _:
                    raise RuntimeError("invalid copmile target option: " + key)
        
        # print(dir(build_target))
        self.target_tree[target_config['name']]['builder'] = build_target
    
    binary_dir: str = ""
    target_tree: dict = {}

# create a target to compile
class BuildTarget:
    # def __init__(self, target_name: str, compiler: Compiler):
    def __init__(self, target_name: str, build_command: callable):
        # self.target_name = target_name
        self.target_name = target_name
        self.build_command = build_command
        # compiler
        pass
    
    def build(self):
        self.build_command (
            self.src_files,
            self.link_dirs,
            self.include_dirs,
            self.compiler_flags,
            self.build_dir,
            self.target_name
        )
    
    # add source files to the target
    def add_source_file(self, file_path: str):
        self.src_files.append(file_path)
    
    def add_source_files(self, file_paths: list[str]):
        self.src_files.extend(file_paths)
    
    # add link directory to target
    def add_link_dir(self, dir_path: str):
        self.link_dirs.append(dir_path)
    
    def add_link_dirs(self, dir_paths: list[str]):
        self.link_dirs.extend(dir_paths)
    
    # add included directories to the target 
    def add_include_dir(self, dir_path: str):
        self.include_dirs.append(dir_path)
    
    def add_include_dirs(self, dir_paths: list[str]):
        self.include_dirs.extend(dir_paths)
    
    # aadd aa compiler flag manually
    def add_compiler_flag(self, flag: str):
        self.compiler_flags.append(flag)
    
    def add_compiler_flags(self, flags: list[str]):
        self.compiler_flags.extend(flags)
    
    # needs change
    def set_build_dir(self, path: str, mkdir_if_not_exists = True):
        self.build_dir = path
        
    
    target_name: str = ""
    src_files: list[str] = list()
    include_dirs: list[str] = list()
    link_dirs: list[str] = list()
    compiler_flags: list[str] = list()
    # compiler: toolchains.Compiler
    build_dir: os.PathLike = ""
    build_command: callable = None
    # dependencies: list[BuildTarget()]

def gcc_compiler_command(
    # compiler_path: os.PathLike,
    src_files: list[os.PathLike],
    link_dirs: list[os.PathLike],
    include_dirs: list[os.PathLike],
    compiler_flags: list[str],
    build_dir: os.PathLike,
    target_name: str
):  
    if not os.path.isdir(build_dir):
        os.system('mkdir ' + build_dir)
    srcs = ' '.join(src_files)
    cmpflags = ' '.join(compiler_flags)
    linkd = ' '.join(link_dirs)
    incld = '-L' + ';'.join(include_dirs) + ' '
    
    # c_or_cpp = None
    # if srcs[0].endswith(['.cpp', '.cxx']):
    #     c_or_cpp = 'g++'
    # else
    
    command = ' '.join(["g++", srcs, cmpflags, linkd, incld]) + '-o ' + build_dir + target_name
    
    print("command to be run ->\n" + command)
    
    os.system(command)
    

GCC_Compiler = BuildTarget(
    "gcc",
    gcc_compiler_command 
)



# GCC_Compiler: toolchains.Compiler = toolchains.Compiler("gcc")


