import subprocess
import os
import sys
import shutil
import winreg
from common_vars import *
vs_intermediate     = "_vs_tmp"
grpc_path    = "../grpc"
prefix_path         = "_prefix"

#path to unreal source root folder, against which grpc will be build

def clone_grpc_win():
    current_path = os.path.realpath(__file__)
    dir_name = os.path.dirname(current_path)
    os.chdir(dir_name)
    abs_path = os.path.abspath("../")
    print("clone_grpc abs_path: " +abs_path)
    print("clone_grpc abs_path: " +abs_path+"\\grpc-source-win")
    

    if os.path.exists("../grpc-source-win"):
        shutil.rmtree("../grpc-source-win", True)
        os.rmdir(abs_path+"\\grpc-source-win")
    
    os.chdir(abs_path)
    cmd_line = ["git", "clone", "--recursive", "https://github.com/grpc/grpc.git", "grpc-source-win"]
    subprocess.call(cmd_line)

    cmd_checkout = ["git", "checkout", "v1.12.x"]
    os.chdir(abs_path+"/grpc-source-win")
    subprocess.call(cmd_checkout)
    
    os.chdir(dir_name)

def create_build_prj():
    abs_path = os.path.abspath("../grpc-source-win")
    c_make_lists = abs_path + "/CMakeLists.txt"
    print("c_make_lists: " +c_make_lists)
    cmd_line = ["cmake", "-G", "Visual Studio 15 2017 Win64"]
    #install prefix
    #cmd_line.append("-DCMAKE_INSTALL_PREFIX="+os.path.join(os.getcwd(), prefix_path))
    cmd_line.append("-DCMAKE_BUILD_TYPE=Release")
    cmd_line.append("-DCMAKE_CONFIGURATION_TYPES=Release")
    cmd_line.append("-Dprotobuf_BUILD_TESTS=false")
    cmd_line.append("-Dprotobuf_MSVC_STATIC_RUNTIME=false")
    cmd_line.append("-Dprotobuf_MSVC_STATIC_RUNTIME=false")
    cmd_line.append("-DgRPC_ZLIB_PROVIDER=package")
    cmd_line.append("-DgRPC_SSL_PROVIDER=package")
    cmd_line.append("-DLIB_EAY_DEBUG=" + unreal_path + "/ThirdParty/OpenSSL/1_0_2h/lib/Win64/VS2015/libeay64_static.lib")
    cmd_line.append("-DLIB_EAY_LIBRARY_DEBUG=" + unreal_path + "/ThirdParty/OpenSSL/1_0_2h/lib/Win64/VS2015/libeay64_static.lib")
    cmd_line.append("-DLIB_EAY_LIBRARY_RELEASE=" + unreal_path + "/ThirdParty/OpenSSL/1_0_2h/lib/Win64/VS2015/libeay64_static.lib")
    cmd_line.append("-DLIB_EAY_RELEASE=" + unreal_path + "/ThirdParty/OpenSSL/1_0_2h/lib/Win64/VS2015/libeay64_static.lib")
    cmd_line.append("-DOPENSSL_INCLUDE_DIR=" + unreal_path + "/ThirdParty/OpenSSL/1_0_2h/include/Win64/VS2015")
    cmd_line.append("-DSSL_EAY_DEBUG=" + unreal_path + "/ThirdParty/OpenSSL/1_0_2h/lib/Win64/VS2015/ssleay64_static.lib")
    cmd_line.append("-DSSL_EAY_LIBRARY_DEBUG=" + unreal_path + "/ThirdParty/OpenSSL/1_0_2h/lib/Win64/VS2015/ssleay64_static.lib")
    cmd_line.append("-DSSL_EAY_LIBRARY_RELEASE=" + unreal_path + "/ThirdParty/OpenSSL/1_0_2h/lib/Win64/VS2015/ssleay64_static.lib")
    cmd_line.append("-DSSL_EAY_RELEASE=" + unreal_path + "/ThirdParty/OpenSSL/1_0_2h/lib/Win64/VS2015/ssleay64_static.lib")
    cmd_line.append("-DZLIB_INCLUDE_DIR=" + unreal_path + "/ThirdParty/zlib/v1.2.8/include/Win64/VS2015")
    cmd_line.append("-DZLIB_LIBRARY_DEBUG=" + unreal_path + "/ThirdParty/zlib/v1.2.8/lib/Win64/VS2015/zlibstatic.lib")
    cmd_line.append("-DZLIB_LIBRARY_RELEASE=" + unreal_path + "/ThirdParty/zlib/v1.2.8/lib/Win64/VS2015/zlibstatic.lib")
    cmd_line.append(c_make_lists)
    
    print("path test: " +abs_path)
    if os.path.exists(abs_path+"/.winbuild"):
        shutil.rmtree(abs_path+"/.winbuild", True)
    os.chdir(abs_path)
    subprocess.call(cmd_line)
    cmd_build_libs = [msbuild, "grpc.sln"]
    subprocess.call(cmd_build_libs)

    current_path = os.path.realpath(__file__)
    dir_name = os.path.dirname(current_path)

def copy_library_win64():
    current_path = os.path.realpath(__file__)
    dir_name = os.path.dirname(current_path)
    print("copy_library_win64 current_path: " +dir_name)
    os.chdir(dir_name)
    abs_path = os.path.abspath("../")
    print("copy_library_win64: " +abs_path)
    
    if(os.path.exists(abs_path + "/Plugins/GRPC/Source/ThirdParty/Win64/")):
        shutil.rmtree(abs_path + "/Plugins/GRPC/Source/ThirdParty/Win64/", True)
    
    shutil.copytree(abs_path + "/grpc-source-win/Release/", abs_path + "/Plugins/GRPC/Source/ThirdParty/Win64/")
    shutil.copytree(abs_path + "/grpc-source-win/include/", abs_path + "/Plugins/GRPC/Source/ThirdParty/Win64/include")
    
    return 0
    
##################################################

#create intermediate path


clone_grpc_win()
#create vs project files
create_build_prj()

#build vs project 
copy_library_win64()

