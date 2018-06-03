# ue-grpc
Python scripits for building Unreal Engine compatibile gRPC library.


WORK IN PROGRESS

Scripts only support cross compilation tool-chain provided with Unreal Engine. 
It's currently not possible to compile from under Linux or MacOS.

Make sure you have corss chain installed:
https://docs.unrealengine.com/en-us/Platforms/Linux/GettingStarted

I tested only with latest version (clang 5.0 as of writting).

Make sure you have those dependencies installed for Windows:

https://github.com/grpc/grpc/blob/master/INSTALL.md

Also you should install Python 3>

To build for Linux, you need to build Windows binaries first. 
As a Linux Build depends on some generated code, which can only be generated when protoc is present.

In common_vars.py
Set Path to Unreal Source against which you will build.
Set Path to MS build. The easiest way to obtain it is to open Developer Console and type "where msbuild". Path Visual Studio will be the right one.

The easiest way to build everything in right order will be using build_all.py (once finished).


Also make sure to have at least 4 GB of space for build.  For each build scripts pull different repository, as generating Windows build is not compatibile with Linux.