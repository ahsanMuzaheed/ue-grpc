// Copyright 1998-2015 Epic Games, Inc. All Rights Reserved.
using System;
using System.IO;
using System.Text.RegularExpressions;

namespace UnrealBuildTool.Rules
{
	public class GRPC : ModuleRules
	{
		public GRPC(ReadOnlyTargetRules Target) : base(Target)
		{
		    PrivateIncludePaths.AddRange(
            new string[] {
            "GRPC/Private",
            }
            );


        PublicDependencyModuleNames.AddRange(
            new string[]
            {
            "Core",
            "Projects",
			"OpenSSL",
			"zlib"
            }
            );


        PrivateDependencyModuleNames.AddRange(
            new string[]
            {
            }
            );


        DynamicallyLoadedModuleNames.AddRange(
            new string[]
            {
            }
            );
			
		

            if (Target.Type == TargetRules.TargetType.Server)
            {
                if (Target.Platform == UnrealTargetPlatform.Linux)
                {
                    string BaseDirectory = System.IO.Path.GetFullPath(System.IO.Path.Combine(ModuleDirectory, ".."));
                    string SDKDirectory = System.IO.Path.Combine(BaseDirectory, "ThirdParty", "x86_64-unknown-linux-gnu");
                    PublicIncludePaths.Add(System.IO.Path.Combine(SDKDirectory, "include"));
                    PublicDefinitions.Add("ENABLE_GRPC=1"); //hack
                    PublicDefinitions.Add("GPR_FORBID_UNREACHABLE_CODE=1");
                    PublicLibraryPaths.Add(SDKDirectory);
                    // PublicAdditionalLibraries.Add(System.IO.Path.Combine(SDKDirectory, "libares.a"));
                    // PublicAdditionalLibraries.Add(System.IO.Path.Combine(SDKDirectory, "libcares.a"));
                    PublicAdditionalLibraries.Add(System.IO.Path.Combine(SDKDirectory, "libaddress_sorting.a"));
                    PublicAdditionalLibraries.Add(System.IO.Path.Combine(SDKDirectory, "libgpr.a"));

                    PublicAdditionalLibraries.Add(System.IO.Path.Combine(SDKDirectory, "libgrpc.a"));
                    PublicAdditionalLibraries.Add(System.IO.Path.Combine(SDKDirectory, "libgrpc_cronet.a"));
                   // PublicAdditionalLibraries.Add(System.IO.Path.Combine(SDKDirectory, "libgrpc_plugin_support.a"));
                    PublicAdditionalLibraries.Add(System.IO.Path.Combine(SDKDirectory, "libgrpc_unsecure.a"));
                    PublicAdditionalLibraries.Add(System.IO.Path.Combine(SDKDirectory, "libgrpc++.a"));
                   // PublicAdditionalLibraries.Add(System.IO.Path.Combine(SDKDirectory, "libgrpc++_core_stats.a"));
                    PublicAdditionalLibraries.Add(System.IO.Path.Combine(SDKDirectory, "libgrpc++_cronet.a"));
                   // PublicAdditionalLibraries.Add(System.IO.Path.Combine(SDKDirectory, "libgrpc++_error_details.a"));
                    //PublicAdditionalLibraries.Add(System.IO.Path.Combine(SDKDirectory, "libgrpc++_reflection.a"));
                    PublicAdditionalLibraries.Add(System.IO.Path.Combine(SDKDirectory, "libgrpc++_unsecure.a"));
                    PublicAdditionalLibraries.Add(System.IO.Path.Combine(SDKDirectory, "libprotobuf.a"));
                   // PublicAdditionalLibraries.Add(System.IO.Path.Combine(SDKDirectory, "libprotobuf-lite.a"));
                   // PublicAdditionalLibraries.Add(System.IO.Path.Combine(SDKDirectory, "libprotoc.a"));
                }
                else
                {
                    PublicDefinitions.Add("ENABLE_GRPC=0");
                }
            }
			else if(Target.Platform == UnrealTargetPlatform.Win64)
            {
                PublicDefinitions.Add("ENABLE_GRPC=1"); //hack

                string BaseDirectory = System.IO.Path.GetFullPath(System.IO.Path.Combine(ModuleDirectory, ".."));
                string SDKDirectory = System.IO.Path.Combine(BaseDirectory, "ThirdParty", "Win64");
                PublicIncludePaths.Add(System.IO.Path.Combine(SDKDirectory, "include"));
                PublicDefinitions.Add("ENABLE_GRPC=1"); //hack
                PublicDefinitions.Add("GPR_FORBID_UNREACHABLE_CODE=1");
                PublicLibraryPaths.Add(SDKDirectory);
                // PublicAdditionalLibraries.Add(System.IO.Path.Combine(SDKDirectory, "libares.a"));
                PublicAdditionalLibraries.Add(System.IO.Path.Combine(SDKDirectory, "cares.lib"));
                PublicAdditionalLibraries.Add(System.IO.Path.Combine(SDKDirectory, "address_sorting.lib"));
                PublicAdditionalLibraries.Add(System.IO.Path.Combine(SDKDirectory, "gpr.lib"));

                PublicAdditionalLibraries.Add(System.IO.Path.Combine(SDKDirectory, "grpc.lib"));
                PublicAdditionalLibraries.Add(System.IO.Path.Combine(SDKDirectory, "grpc_cronet.lib"));
                // PublicAdditionalLibraries.Add(System.IO.Path.Combine(SDKDirectory, "libgrpc_plugin_support.a"));
                PublicAdditionalLibraries.Add(System.IO.Path.Combine(SDKDirectory, "grpc_unsecure.lib"));
                PublicAdditionalLibraries.Add(System.IO.Path.Combine(SDKDirectory, "grpc++.lib"));
                // PublicAdditionalLibraries.Add(System.IO.Path.Combine(SDKDirectory, "libgrpc++_core_stats.a"));
                PublicAdditionalLibraries.Add(System.IO.Path.Combine(SDKDirectory, "grpc++_cronet.lib"));
                PublicAdditionalLibraries.Add(System.IO.Path.Combine(SDKDirectory, "grpc++_error_details.lib"));
                PublicAdditionalLibraries.Add(System.IO.Path.Combine(SDKDirectory, "grpc++_reflection.lib"));
                PublicAdditionalLibraries.Add(System.IO.Path.Combine(SDKDirectory, "grpc++_unsecure.lib"));
                PublicAdditionalLibraries.Add(System.IO.Path.Combine(SDKDirectory, "libprotobuf.lib"));
                // PublicAdditionalLibraries.Add(System.IO.Path.Combine(SDKDirectory, "libprotobuf-lite.a"));
                // PublicAdditionalLibraries.Add(System.IO.Path.Combine(SDKDirectory, "libprotoc.a"));
            }
            else
            {
                PublicDefinitions.Add("ENABLE_GRPC=0");
            }
		}
	}
}
