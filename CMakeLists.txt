cmake_minimum_required(VERSION 2.8.9)
project (icon_extractor)
add_library(icon_extractor SHARED src/icon_extractor.cpp)

install(
	TARGETS icon_extractor 
	CONFIGURATIONS Debug Release 
	DESTINATION "${CMAKE_SOURCE_DIR}/bin"
)
	
