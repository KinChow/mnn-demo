cmake_minimum_required(VERSION 3.20)

set(DEBUG_VERSION "DebugMode")
set(RELEASE_VERSION "ReleaseMode")
set(COMPILE_MODE ${DEBUG_VERSION})
set(PROJECT_NAME "LinearRegression")

# debug mode (project name + compile time)
if(${COMPILE_MODE} MATCHES ${DEBUG_VERSION})
    set(USE_RELEASE_MODE 0)
    set(CMAKE_BUILD_TYPE "Debug")
# release mode (project name + version)
else()
    set(USE_RELEASE_MODE 1)
    set(CMAKE_BUILD_TYPE "Release")
endif()

string(TIMESTAMP COMPILE_TIME %y%m%d_%H%M%S)
set(VERSION_MAJOR 0)
set(VERSION_MINOR 0)
set(VERSION_PATCH 0)
set(VERSION_TWEAK 2)

project(${PROJECT_NAME})

set(CMAKE_CXX_STANDARD 17)

set(MNN_DIR ${PROJECT_SOURCE_DIR}/../MNN)

set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -Wall -Werror -O3 -save-temps")

configure_file(
    "${PROJECT_SOURCE_DIR}/include/config.h.in"
    "${PROJECT_BINARY_DIR}/config.h"
)

include_directories(
    ${PROJECT_SOURCE_DIR}/include
    ${PROJECT_BINARY_DIR}
    ${MNN_DIR}/include
)

if(ANDROID)
    set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -frtti -fexceptions")
    link_directories(${MNN_DIR}/libs/android)
elseif(UNIX)
    link_directories(${MNN_DIR}/libs/linux)
endif()

aux_source_directory(${PROJECT_SOURCE_DIR}/src SRC_DIR)

add_executable(${PROJECT_NAME} ${SRC_DIR})

target_link_libraries(${PROJECT_NAME} MNN)

set(EXECUTABLE_OUTPUT_PATH ${PROJECT_SOURCE_DIR}/output)
