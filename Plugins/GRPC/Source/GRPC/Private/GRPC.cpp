// Copyright 1998-2015 Epic Games, Inc. All Rights Reserved.

#include "IGRPC.h"

#if ENABLE_GRPC

#endif
#include "grpcpp/grpcpp.h"
class FGRPC : public IGRPC
{
	/** IModuleInterface implementation */
	virtual void StartupModule() override;
	virtual void ShutdownModule() override;
};

IMPLEMENT_MODULE( FGRPC, GRPC)



void FGRPC::StartupModule()
{
#if ENABLE_GRPC
	
#endif
	grpc::string out = grpc::Version();
	FString ver = FString(ANSI_TO_TCHAR(out.c_str()));
	UE_LOG(LogTemp, Warning, TEXT("FGRPC::StartupModule Version: %s "), *ver);
}


void FGRPC::ShutdownModule()
{
	// This function may be called during shutdown to clean up your module.  For modules that support dynamic reloading,
	// we call this function before unloading the module.
}
