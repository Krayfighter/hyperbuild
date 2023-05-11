

# from ctypes import c_char
import os

import enum
import typing


# create a target to compile
class BuildTarget:
    # def __init__(self, target_name: str, compiler: Compiler):
    def __init__(self, target_name: str, build_command: callable):
        # self.target_name = target_name
        self.target_name = target_name
        self.build_command = build_command
        # self.src_files = []
        # compiler
        # pass
    
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
    def set_build_dir(self, path: str):
        self.build_dir = path
        
    
    target_name: str = ""
    src_files: list[str] = []
    include_dirs: list[str] = []
    link_dirs: list[str] = []
    compiler_flags: list[str] = []
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
    incld = '-I' + ' -I'.join(include_dirs) + ' '
    
    print(build_dir)
    print(target_name)
    
    # if 
    print('------------------')
    print(srcs)
    print(cmpflags)
    print(linkd)
    print(incld)
    
    command = ' '.join(["g++", srcs, cmpflags, linkd, incld]) + '-o ' + build_dir + target_name
    
    print("command to be run ->\n" + command)
    
    os.system(command)
    

# might end up deprecating aat some point
GCC_Compiler = BuildTarget(
    "gcc",
    gcc_compiler_command 
)


class enum_target_types(enum.Enum):
    TARGET_ROOT = 1
    TARGET_DEP = 2


class target_t(typing.TypedDict):
    name: str
    builder: BuildTarget
    target_type: enum_target_types
    dependencies: list[str] # the string should be valid defined target name



# class defining a full project with possibly multiple different targets
class Project:
    def __init__(self, config: dict):
        self.name = config['project']['name']
        self.set_binary_dir(config['project']['binary_dir'])
        self.parse_targets(config['target'])
        # print(self.targets)
        # self.resolve_deps(config['deps'], self.target_tree)
    
    def set_binary_dir(self, path: str):
        if not os.path.isdir(path):
            os.system('mkdir ' + path)
            # raise RuntimeError("binary dTARGET_ROOToes not exists for project")
        self.binary_dir = path
    
    # def add_target(target, dependencies = []):
    #     pass
    
    def build(self):
        # self.target_tree['main']['builder'].build()
        # print(type(self.targets))
        # print(self.targets)
        for name, target in self.targets.items():
            # print(target)
            if target['target_type'] == enum_target_types.TARGET_ROOT:
                for dep in target['dependencies']:
                    self.build_deps(target, dep)
                target['builder'].build()
            else:
                pass
    
    # this function may recurse as to cover a chain or tree of dependencies
    def build_deps(self, dependant: target_t, dependency: str):
        if dependency not in self.built_targets:
            print(dependency)
            if self.targets[dependency]['dependencies'] == []:
                self.targets[dependency]['builder'].build()
            else:
                for dep in self.targets[dependency]['deps']:
                    self.build_deps(dependency, self.targets['dep'])
        else:
            pass
        # TODO add deps build dirs to the link dirs of the dependant
    
    
    def parse_targets(self, target_config: dict):
        
        for targ_name, targ_cfg in target_config.items():
            build_target = BuildTarget(targ_name, gcc_compiler_command)
            print(targ_name)
            print('src files')
            print(build_target.src_files)
            print(targ_cfg)
            target_type = None
            deps = None
            
            # get necessary tags
            # Here means the target_type must be valid type
            if targ_cfg['type'] == 'root':
                target_type = enum_target_types.TARGET_ROOT
            elif targ_cfg['type'] == 'dep':
                target_type = enum_target_types.TARGET_DEP
            else:
                raise RuntimeError("unsupported target type: " + value['type'])

            # try to get deps
            # Here means deps must be valid type
            try:
                deps = targ_cfg['deps']
            except:
                deps = []
            
            # search the keys in the target config
            # WARNING this may pass but let an invalid structer be returned
            # on second thought that might not be the case, this should be checked and possibly fixed later
            for (key, value) in targ_cfg.items():
                match key:
                    case "type":
                        pass
                    case "deps":
                        pass
                    case "build_dir":
                        build_target.set_build_dir(self.binary_dir + value)
                    case "src_files":
                        build_target.add_source_files(value)
                    case "include_dirs":
                        build_target.add_include_dirs(value)
                    case _:
                        raise RuntimeError("invalid copmile target option: " + key)
            
            # add the current configs to the self.targets list aas a new target (should be enforced as valid at runtime)
            self.targets[targ_name] = target_t (
                name = targ_name,
                builder = build_target,
                target_type = target_type,
                dependencies = deps
            )
            
            print(targ_name)
            print('src files')
            print(build_target.src_files)
            print(targ_cfg)
            
            # build_target = None
            
            # print('-----------------------')
            # print(self.targets)
            # print(self.targets[targ_name])
            # print(self.targets[targ_name]['builder'].src_files)
    
    def resolve_deps(self, deps: dict, target: dict):
        if target['deps'] != []:
            for dep in deps:
                pass
                # check if dep has deps
                    # recurse if so
                # else create a new build target for dep and 
    
    binary_dir: str = ""
    targets: dict[str: target_t] = {}
    built_targets: list[str] = []
    # targets: list[target_t] = []
    # built_targets: list[target_t] = []


