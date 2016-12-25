project(testproj)
cmake_minimum_required(VERSION 3.0)

include(${CMAKE_BINARY_DIR}/conanbuildinfo.cmake)
conan_basic_setup()

find_package(Threads)

add_executable(testproj test.cpp)

target_link_libraries(testproj
    ${CONAN_LIBS}
    ${CMAKE_THREAD_LIBS_INIT})
