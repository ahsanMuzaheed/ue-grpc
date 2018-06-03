import subprocess
import os
import sys
import shutil
import winreg
from build_linux import *
from build_win64 import *

#Windows Build START
#clone_grpc_win()
#create vs project files
#create_build_prj()

#build vs project 
copy_library_win64()
#Windows Build  END

#Linux Build START
clone_grpc_linux()
#create intermediate path
if os.path.exists(clang_intermediate):
    shutil.rmtree(clang_intermediate, True)
os.mkdir(clang_intermediate)

#build
if(clang_build_all() != 0):
    print("compiler error!")
    sys.exit(1)

#archive
if(clang_build_static_libs(clang_intermediate) != 0):
    print("archive error!")
    sys.exit(1)

#copy to lib path
copy_libs(clang_intermediate, library_path)
copy_to_plugin()
print("**Done!**")
sys.exit(0)
#Linux Build END