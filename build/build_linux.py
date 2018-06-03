import subprocess
import os
import sys
import shutil
import winreg
from common_vars import *
from source_file_paths import *

clang_linux_root    = os.path.join(os.environ["LINUX_MULTIARCH_ROOT"], "x86_64-unknown-linux-gnu")
clang_exe           = clang_linux_root + "/bin/clang.exe"
clang_ar_exe        = clang_linux_root + "/bin/x86_64-unknown-linux-gnu-ar.exe"
clang_ranlib_exe    = clang_linux_root + "/bin/x86_64-unknown-linux-gnu-ranlib.exe"
clang_intermediate  = "_clang_tmp"
#path to unreal root folder, against which grpc will be build

library_path        = "../grpc/lib/linux"
lib_protobuf_file        = "libprotobuf.a"
lib_cares_file      = "libcares.a"
lib_address_sorting_file = "libaddress_sorting.a"
lib_grp_file        = "libgpr.a" 
lib_grpc_core_file        = "libgrpc.a"

lib_grpc_cronet_file = "libgrpc_cronet.a"
lib_grpc_unsecure_file = "libgrpc_unsecure.a"
lib_grpc_cpp_file = "libgrpc++.a"
lib_grpc_cpp_core_stats_file = "libgrpc++_core_stats.a"
lib_grpc_cpp_cronet_file = "libgrpc++_cronet.a"
lib_grpc_cpp_unsecure_file = "libgrpc++_unsecure.a"

grpc_win_path = "../grpc-source-win"

def clone_grpc_linux():
    abs_path = os.path.abspath("..")
    print("clone_grpc abs_path: " +abs_path)
    print("clone_grpc abs_path: " +abs_path+"\\grpc-source-linux")
    

    if os.path.exists("../grpc-source-linux"):
        shutil.rmtree("../grpc-source-linux", True)
        os.rmdir(abs_path+"\\grpc-source-linux")
    
    os.chdir(abs_path)
    cmd_line = ["git", "clone", "--recursive", "https://github.com/grpc/grpc.git", "grpc-source-linux"]
    subprocess.call(cmd_line)

    cmd_checkout = ["git", "checkout", "v1.12.x"]
    os.chdir(abs_path+"/grpc-source-linux")
    subprocess.call(cmd_checkout)
    
    os.chdir(abs_path+"/build")

def get_abs_grpc_path():
    return os.path.abspath(grpc_src_path)

def get_abs_plugin_path():
    path = os.path.abspath("../")
    return path + "/Plugins/GRPC/Source/ThirdParty/x86_64-unknown-linux-gnu"

def copy_libs_to_plugin(from_path, lib_name):
    source_lib_file_path = from_path+"/"+lib_name
    target_lib_file_path = get_abs_plugin_path()+"/"+lib_name
    #if(not os.path.exists(target_path)):
    #    os.makedirs(target_path)
    print("Copy " + source_lib_file_path + " to " + target_lib_file_path)
    shutil.copy(source_lib_file_path, target_lib_file_path)

def get_protc():
    return grpc_win_path+ "/.winbuild/third_party/protobuf/Release/protoc.exe"

def get_grpc_plugin():
    return grpc_win_path + "/.winbuild/Release/grpc_cpp_plugin.exe"

def generate_proto_files():
    protoc = get_protc()
    proto_src = grpc_src_path+"/src/proto/channelz/channelz.proto"
    out_path = grpc_src_path+".gens"
    grpc_plug = get_grpc_plugin()
    cmd_line = [protoc]
    cmd_line.append("--grpc_out=generate_mock_code=true:"+out_path)
    cmd_line.append("--cpp_out="+out_path)
    cmd_line.append("--plugin=protoc-gen-grpc="+grpc_plug)
    cmd_line.append(" -I . -I " + proto_src)
    #--grpc_out=generate_mock_code=true:D:/GitHub/ue-grpc/grpc-source/.winbuild/gens -
    # -cpp_out=D:/GitHub/ue-grpc/grpc-source/.winbuild/gens 
    #--plugin=protoc-gen-grpc=D:/GitHub/ue-grpc/grpc-source/.winbuild/Debug/grpc_cpp_plugin.exe -I . -I D:/GitHub/ue-grpc/grpc-source/third_party/protobuf/src src/proto/grpc/status/status.proto
    if(subprocess.call(cmd_line) !=0 ):
        return 1
    return 0
    
def clang_build_static_lib(source_files, intermediate_path, static_lib_name):
    object_files=[]
    lib_file_path=intermediate_path+"/"+static_lib_name
    
    for cpp_file_path in source_files:
        #object file
        cpp_file = os.path.split(cpp_file_path)[1];
        out_file = intermediate_path + "/" + os.path.splitext(cpp_file)[0] + ".o"
        object_files.append(out_file)
    
    ar_cmd_line=[clang_ar_exe,  "sru", lib_file_path]
    ar_cmd_line.extend(object_files)
    print("archive to " + static_lib_name)
    if(subprocess.call(ar_cmd_line)!=0 or subprocess.call([clang_ranlib_exe, lib_file_path])!=0):
        return 1
    return 0


    

def copy_library(intermediate_path, target_path, lib_name):
    source_lib_file_path = intermediate_path+"/"+lib_name
    target_lib_file_path = target_path+"/"+lib_name
    if(not os.path.exists(target_path)):
        os.makedirs(target_path)
    print("Copy " + source_lib_file_path + " to " + target_lib_file_path)
    shutil.copy(source_lib_file_path, target_lib_file_path)

def clang_build_grpc_generic(source_files, intermediate_path):
    for cpp_file_path in source_files:
        #output file
        cpp_file = os.path.split(cpp_file_path)[1];
        out_file = intermediate_path + "/" + os.path.splitext(cpp_file)[0] + ".o"
        cmd_line=[clang_exe, "-c", "-o", out_file]
        abs_path = get_abs_grpc_path()
        print("path to grpc source: " + abs_path)
        #stdand c++ library
        cmd_line.append("-std=c++14")
        cmd_line.append("-nostdinc++")
        cmd_line.append("-fPIC")
        cmd_line.append("-I"+unreal_path+"/ThirdParty/Linux/LibCxx/include/")
        cmd_line.append("-I"+unreal_path+"/ThirdParty/Linux/LibCxx/include/c++/v1")
        cmd_line.append("-I" + abs_path + "/include")
        cmd_line.append("-I" + abs_path)
        cmd_line.append("-include"+abs_path+"/third_party/cares/config_linux/ares_config.h")
        cmd_line.append("-I" + abs_path + "/third_party/address_sorting/include")
        cmd_line.append("-I" + abs_path + "/third_party/cares/cares")
        cmd_line.append("-I" + abs_path + "/third_party/cares/")
        cmd_line.append("-I" + abs_path + "/third_party/protobuf/src/")
        cmd_line.append("-I"+clang_linux_root+"/usr/include")
        cmd_line.append("-I"+unreal_path+"/ThirdParty/zlib/v1.2.8/include/Linux/x86_64-unknown-linux-gnu")
        
        cmd_line.append("-I"+unreal_path+"/ThirdParty/OpenSSL/1_0_2h/include/Linux/x86_64-unknown-linux-gnu")
        #cmd_line.append("-L"+unreal_source+"/ThirdParty/zlib/v1.2.8/lib/Linux/x86_64-unknown-linux-gnu")

        #add c++ compiler flags
        cmd_line.extend(["-Wall", "-Werror", "-funwind-tables", "-Wsequence-point", "-fno-math-errno", "-fno-rtti", "-fdiagnostics-format=msvc"])
        cmd_line.extend(["-Wdeprecated-register", "-Wno-unused-private-field", "-Wno-tautological-compare", "-Wno-undefined-bool-conversion", "-Wno-unused-local-typedef"])
        cmd_line.extend(["-Wno-inconsistent-missing-override", "-Wno-undefined-var-template", "-Wno-delete-non-virtual-dtor", "-Wno-expansion-to-defined", "-Wno-null-dereference"])
        cmd_line.extend(["-Wno-literal-conversion", "-Wno-unused-variable", "-Wno-unused-function", "-Wno-switch", "-Wno-unknown-pragmas", "-Wno-invalid-offsetof"]) 
        cmd_line.extend(["-Wno-gnu-string-literal-operator-template", "-Wshadow", "-Wno-error=shadow", "-Wno-deprecated-register", "-Wconstant-conversion", "-Wc++11-narrowing"]) 
        cmd_line.extend(["-gdwarf-3", "-O2", "-fno-exceptions"]) 

        #add target define 
        cmd_line.extend(["-DPLATFORM_EXCEPTIONS_DISABLED=1", "-D_LINUX64"])
        cmd_line.append("--target=x86_64-unknown-linux-gnu")
        cmd_line.append("--sysroot=\""+ clang_linux_root +"\"")

        #c++ 11
        cmd_line.extend(["-x", "c++", "-std=c++11"]) 
        
        #google protobuf source include
        #google protobuf defines
        cmd_line.append("-DGOOGLE_PROTOBUF_NO_RTTI=1")
        cmd_line.append("-D__STDC_LIMIT_MACROS")
        cmd_line.append("-D__STDC_CONSTANT_MACROS")
        cmd_line.append("-DPB_FIELD_32BIT=1")
        cmd_line.append("-DADDRESS_SORTING_POSIX=1")
        cmd_line.append("-DADDRESS_SORTING_WINDOWS=0")
        #pthread
        cmd_line.extend(["-pthread", "-DHAVE_PTHREAD=1"])

        
        #finaly, add source file
        cmd_line.append(cpp_file_path)
        print("compiler " + cpp_file + "...")
        
        #run clang++
        if(subprocess.call(cmd_line) !=0 ):
            return 1
    return 0

def clang_build_cares(source_files, intermediate_path):
    for cpp_file_path in source_files:
        #output file
        cpp_file = os.path.split(cpp_file_path)[1];
        out_file = intermediate_path + "/" + os.path.splitext(cpp_file)[0] + ".o"
        cmd_line=[clang_exe, "-c", "-o", out_file]
        abs_path = get_abs_grpc_path()
        #stdand c++ library
        cmd_line.append("-std=c++14")
        cmd_line.append("-nostdinc++")
        cmd_line.append("-fPIC")
        cmd_line.append("-I"+unreal_path+"/ThirdParty/Linux/LibCxx/include/")
        cmd_line.append("-I"+unreal_path+"/ThirdParty/Linux/LibCxx/include/c++/v1")
        cmd_line.append("-I" + abs_path + "/include")
        cmd_line.append("-I" + abs_path)
        cmd_line.append("-include"+abs_path+"/third_party/cares/config_linux/ares_config.h")
        cmd_line.append("-I" + abs_path + "/third_party/address_sorting/include")
        cmd_line.append("-I" + abs_path + "/third_party/cares/cares")
        cmd_line.append("-I" + abs_path + "/third_party/cares/")
        cmd_line.append("-I" + abs_path + "/grpc-source/third_party/protobuf/src/")
        
        cmd_line.append("-I"+clang_linux_root+"/usr/include")
        cmd_line.append("-I"+unreal_path+"/ThirdParty/zlib/v1.2.8/include/Linux/x86_64-unknown-linux-gnu")
        
        cmd_line.append("-I"+unreal_path+"/ThirdParty/OpenSSL/1_0_2h/include/Linux/x86_64-unknown-linux-gnu")
        #cmd_line.append("-L"+unreal_source+"/ThirdParty/zlib/v1.2.8/lib/Linux/x86_64-unknown-linux-gnu")

        #add c++ compiler flags
        cmd_line.extend(["-Wall", "-funwind-tables", "-Wsequence-point", "-fno-math-errno", "-fno-rtti", "-fdiagnostics-format=msvc"])
        cmd_line.extend(["-Wdeprecated-register", "-Wno-unused-private-field", "-Wno-tautological-compare", "-Wno-undefined-bool-conversion", "-Wno-unused-local-typedef"])
        cmd_line.extend(["-Wno-inconsistent-missing-override", "-Wno-undefined-var-template", "-Wno-delete-non-virtual-dtor", "-Wno-expansion-to-defined", "-Wno-null-dereference"])
        cmd_line.extend(["-Wno-literal-conversion", "-Wno-unused-variable", "-Wno-unused-function", "-Wno-switch", "-Wno-unknown-pragmas", "-Wno-invalid-offsetof"]) 
        cmd_line.extend(["-Wno-gnu-string-literal-operator-template", "-Wshadow", "-Wno-error=shadow", "-Wno-deprecated-register", "-Wconstant-conversion", "-Wc++11-narrowing"]) 
        cmd_line.extend(["-gdwarf-3", "-O2", "-fno-exceptions"])
        cmd_line.extend(["-pedantic", "-Wextra", "-Wpointer-arith", "-Wwrite-strings", "-Winline", "-Wnested-externs", "-Wmissing-declarations", "-Wmissing-prototypes", "-Wno-long-long"])
        cmd_line.extend(["-Wfloat-equal", "-Wno-multichar", "-Wsign-compare", "-Wundef", "-Wno-format-nonliteral", "-Wendif-labels", "-Wstrict-prototypes", "-Wdeclaration-after-statement", "-Wno-system-headers", "-Wshorten-64-to-32", "-Wunused"])
        #add target define 
        cmd_line.extend(["-DPLATFORM_EXCEPTIONS_DISABLED=1", "-D_LINUX64"])
        cmd_line.append("--target=x86_64-unknown-linux-gnu")
        cmd_line.append("--sysroot=\""+ clang_linux_root +"\"")
        
        #c++ 11
        cmd_line.extend(["-x", "c", "-std=c99"]) 
        
        #google protobuf source include
        #google protobuf defines
        #-D_GNU_SOURCE -D_POSIX_C_SOURCE=199309L -D_XOPEN_SOURCE=600
        cmd_line.append("-D_GNU_SOURCE=1")
        cmd_line.append("-D_POSIX_C_SOURCE=199309L")
        cmd_line.append("-D_XOPEN_SOURCE=600")
        
        # -DWIN32_LEAN_AND_MEAN -D_HAS_EXCEPTIONS=0 -DNOMINMAX
        
        #pthread
        cmd_line.extend(["-pthread", "-DHAVE_PTHREAD=1"])

        
        #finaly, add source file
        cmd_line.append(cpp_file_path)
        print("compiler " + cpp_file + "...")
        
        #run clang++
        if(subprocess.call(cmd_line) !=0 ):
            return 1
    return 0

def clang_build_address_sorting(source_files, intermediate_path):
    for cpp_file_path in source_files:
        #output file
        cpp_file = os.path.split(cpp_file_path)[1];
        out_file = intermediate_path + "/" + os.path.splitext(cpp_file)[0] + ".o"
        cmd_line=[clang_exe, "-c", "-o", out_file]

        #stdand c++ library
        cmd_line.append("-fPIC")
        cmd_line.append("-I"+unreal_path+"/ThirdParty/Linux/LibCxx/include/")
        cmd_line.append("-I"+unreal_path+"/ThirdParty/Linux/LibCxx/include/c++/v1")
        cmd_line.append("-ID:/GitHub/ue-grpc/grpc-source/include")
        cmd_line.append("-ID:/GitHub/ue-grpc/grpc-source")
        cmd_line.append("-ID:/GitHub/ue-grpc/grpc-source/third_party/address_sorting/include")
        cmd_line.append("-ID:/GitHub/ue-grpc/grpc-source/third_party/cares/cares")
        cmd_line.append("-ID:/GitHub/ue-grpc/grpc-source/third_party/cares/")
        
        cmd_line.append("-I"+clang_linux_root+"/usr/include")
        cmd_line.append("-I"+unreal_path+"/ThirdParty/zlib/v1.2.8/include/Linux/x86_64-unknown-linux-gnu")
        cmd_line.append("-I"+unreal_path+"/ThirdParty/OpenSSL/1_0_2h/include/Linux/x86_64-unknown-linux-gnu")
        #cmd_line.append("-L"+unreal_source+"/ThirdParty/zlib/v1.2.8/lib/Linux/x86_64-unknown-linux-gnu")

        #add c++ compiler flags
        cmd_line.extend(["-Wall", "-Werror", "-funwind-tables", "-Wsequence-point", "-fno-math-errno", "-fno-rtti", "-fdiagnostics-format=msvc"])
        cmd_line.extend(["-Wdeprecated-register", "-Wno-unused-private-field", "-Wno-tautological-compare", "-Wno-undefined-bool-conversion", "-Wno-unused-local-typedef"])
        cmd_line.extend(["-Wno-inconsistent-missing-override", "-Wno-undefined-var-template", "-Wno-delete-non-virtual-dtor", "-Wno-expansion-to-defined", "-Wno-null-dereference"])
        cmd_line.extend(["-Wno-literal-conversion", "-Wno-unused-variable", "-Wno-unused-function", "-Wno-switch", "-Wno-unknown-pragmas", "-Wno-invalid-offsetof"]) 
        cmd_line.extend(["-Wno-gnu-string-literal-operator-template", "-Wshadow", "-Wno-error=shadow", "-Wno-deprecated-register", "-Wconstant-conversion", "-Wc++11-narrowing"]) 
        cmd_line.extend(["-gdwarf-3", "-O2", "-fno-exceptions"]) 

        #add target define 
        cmd_line.extend(["-DPLATFORM_EXCEPTIONS_DISABLED=1", "-D_LINUX64"])
        cmd_line.append("--target=x86_64-unknown-linux-gnu")
        cmd_line.append("--sysroot=\""+ clang_linux_root +"\"")

        #c++ 11
        cmd_line.extend(["-x", "c", "-std=c99"]) 
        
        #google protobuf source include
        #google protobuf defines
        cmd_line.append("-DGOOGLE_PROTOBUF_NO_RTTI=1")
        cmd_line.append("-D__STDC_LIMIT_MACROS")
        cmd_line.append("-D__STDC_CONSTANT_MACROS")
        cmd_line.append("-DPB_FIELD_32BIT=1")
        cmd_line.append("-DADDRESS_SORTING_POSIX=1")
        cmd_line.append("-DADDRESS_SORTING_WINDOWS=0")
        #pthread
        cmd_line.extend(["-pthread", "-DHAVE_PTHREAD=1"])

        
        #finaly, add source file
        cmd_line.append(cpp_file_path)
        print("compiler " + cpp_file + "...")
        
        #run clang++
        if(subprocess.call(cmd_line) !=0 ):
            return 1
    return 0

def clang_build_static_libs(intermediate_path):
    retVal = clang_build_static_lib(grpc_core_source_files, intermediate_path, lib_grpc_core_file)
    retVal = clang_build_static_lib(libaddress_sorting_files, intermediate_path, lib_address_sorting_file)
    retVal = clang_build_static_lib(gpr_source_files, intermediate_path, lib_grp_file)
    retVal = clang_build_static_lib(grpc_cronet_files, intermediate_path, lib_grpc_cronet_file)
    retVal = clang_build_static_lib(grpc_unsecure_files, intermediate_path, lib_grpc_unsecure_file)
    retVal = clang_build_static_lib(lib_grpc_cpp_files, intermediate_path, lib_grpc_cpp_file)
    retVal = clang_build_static_lib(lib_grpc_cpp_cronet_files, intermediate_path, lib_grpc_cpp_cronet_file)
    retVal = clang_build_static_lib(lib_grpc_cpp_unsecure_files, intermediate_path, lib_grpc_cpp_unsecure_file)
    retVal = clang_build_static_lib(libproto_files, intermediate_path, lib_protobuf_file)
    retVal = clang_build_static_lib(cares_source_files, intermediate_path, lib_cares_file)
    return retVal

def copy_libs(intermediate_path, target_path):
    copy_library(intermediate_path, target_path, lib_grpc_core_file)
    copy_library(intermediate_path, target_path, lib_address_sorting_file)
    copy_library(intermediate_path, target_path, lib_grp_file)
    copy_library(intermediate_path, target_path, lib_grpc_cronet_file)
    copy_library(intermediate_path, target_path, lib_grpc_unsecure_file)
    copy_library(intermediate_path, target_path, lib_grpc_cpp_file)
    copy_library(intermediate_path, target_path, lib_grpc_cpp_cronet_file)
    copy_library(intermediate_path, target_path, lib_grpc_cpp_unsecure_file)
    copy_library(intermediate_path, target_path, lib_protobuf_file)
    copy_library(intermediate_path, target_path, lib_cares_file)

def clang_build_all():
    result = clang_build_grpc_generic(grpc_core_source_files, clang_intermediate)
    result = clang_build_address_sorting(libaddress_sorting_files, clang_intermediate)
    result = clang_build_grpc_generic(gpr_source_files, clang_intermediate)
    result = clang_build_grpc_generic(grpc_cronet_files, clang_intermediate)
    result = clang_build_grpc_generic(grpc_unsecure_files, clang_intermediate)
    result = clang_build_grpc_generic(lib_grpc_cpp_files, clang_intermediate)
    result = clang_build_grpc_generic(lib_grpc_cpp_cronet_files, clang_intermediate)
    result = clang_build_grpc_generic(lib_grpc_cpp_unsecure_files, clang_intermediate)
    result = clang_build_grpc_generic(libproto_files, clang_intermediate)
    result = clang_build_cares(cares_source_files, clang_intermediate)
    return result

def copy_to_plugin():
    copy_libs_to_plugin(library_path, lib_grpc_core_file)
    copy_libs_to_plugin(library_path, lib_address_sorting_file)
    copy_libs_to_plugin(library_path, lib_grp_file)
    copy_libs_to_plugin(library_path, lib_grpc_cronet_file)
    copy_libs_to_plugin(library_path, lib_grpc_unsecure_file)
    copy_libs_to_plugin(library_path, lib_grpc_cpp_file)
    copy_libs_to_plugin(library_path, lib_grpc_cpp_cronet_file)
    copy_libs_to_plugin(library_path, lib_grpc_cpp_unsecure_file)
    copy_libs_to_plugin(library_path, lib_protobuf_file)
    copy_libs_to_plugin(library_path, lib_cares_file)
    abs_path = os.path.abspath("../")
    print("copy_library_win64: " +abs_path)
    grpc_path = os.path.abspath("../../")
    print("copy_library_win64 grpc: " +grpc_path)
    if(os.path.exists(grpc_path + "/Plugins/GRPC/Source/ThirdParty/x86_64-unknown-linux-gnu/include")):
        shutil.rmtree(grpc_path + "/Plugins/GRPC/Source/ThirdParty/x86_64-unknown-linux-gnu/include", True)
    shutil.copytree(grpc_path + "/grpc-source-win/include/", grpc_path + "/Plugins/GRPC/Source/ThirdParty/x86_64-unknown-linux-gnu/include")

##################################################
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
