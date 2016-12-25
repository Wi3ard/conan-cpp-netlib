project(testproj)
cmake_minimum_required(VERSION 3.0)

include(${CMAKE_BINARY_DIR}/conanbuildinfo.cmake)
conan_basic_setup()

add_executable(testproj test.cpp)

target_link_libraries(testproj ${CONAN_LIBS})
