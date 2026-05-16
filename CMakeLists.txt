cmake_minimum_required(VERSION 3.20)
project(GTASAMultiplayer)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

include_directories(${PROJECT_SOURCE_DIR}/include)

# Server executable
add_executable(sa_server src/server/server.cpp)
target_include_directories(sa_server PRIVATE ${PROJECT_SOURCE_DIR}/include)

if(WIN32)
    target_link_libraries(sa_server ws2_32)
endif()

# Client executable
add_executable(sa_client src/client/client.cpp)
target_include_directories(sa_client PRIVATE ${PROJECT_SOURCE_DIR}/include)

if(WIN32)
    target_link_libraries(sa_client ws2_32)
endif()

# Inject DLL
add_library(sa_inject SHARED src/inject/inject.cpp src/inject/gta_memory.cpp src/inject/ui.cpp)
target_include_directories(sa_inject PRIVATE ${PROJECT_SOURCE_DIR}/include)

if(WIN32)
    target_link_libraries(sa_inject ws2_32)
endif()

# Launcher executable
add_executable(sa_launcher src/inject/launcher.cpp)

if(WIN32)
    target_link_libraries(sa_launcher kernel32)
endif()
