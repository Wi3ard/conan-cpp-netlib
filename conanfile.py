from conans import ConanFile, CMake
from conans.tools import replace_in_file
import os
import shutil

class cppnetlibConan(ConanFile):
    name = "cpp-netlib"
    version = "0.13.0-dev"
    url="https://github.com/Wi3ard/conan-cpp-netlib"
    generators = "cmake", "txt"
    settings = "os", "compiler", "build_type", "arch"
    requires = "Boost/1.60.0@lasote/stable";

    options = {"shared": [True, False],
               "enable_https": [True, False],
               "enable_tests": [True, False],
               "enable_examples": [True, False]}
    default_options = "shared=False", \
        "enable_https=False", \
        "enable_tests=False", \
        "enable_examples=False", \
        "Boost:shared=False"

    def source(self):
        self.run("git clone --recursive https://github.com/cpp-netlib/cpp-netlib.git")
        self.run("cd cpp-netlib && git checkout 0.13-release")

    def config(self):
        if self.options.enable_https:
            self.requires.add("OpenSSL/1.0.2i@lasote/stable", private=False)

    def build(self):
        conan_magic_lines = '''include(GNUInstallDirs)

# Conan.io config
include(${CMAKE_BINARY_DIR}/conanbuildinfo.cmake)
conan_basic_setup()

if(MSVC AND CONAN_LINK_RUNTIME)
  set(flags
    CMAKE_C_FLAGS_DEBUG
    CMAKE_C_FLAGS_MINSIZEREL
    CMAKE_C_FLAGS_RELEASE
    CMAKE_C_FLAGS_RELWITHDEBINFO
    CMAKE_CXX_FLAGS_DEBUG
    CMAKE_CXX_FLAGS_MINSIZEREL
    CMAKE_CXX_FLAGS_RELEASE
    CMAKE_CXX_FLAGS_RELWITHDEBINFO)
  foreach(flag ${flags})
    if(${flag} MATCHES "/MD")
      string(REPLACE "/MDd " "${CONAN_LINK_RUNTIME} " ${flag} "${${flag}}")
      string(REPLACE "/MD " "${CONAN_LINK_RUNTIME} " ${flag} "${${flag}}")
    endif()
  endforeach()
endif()
    '''
        replace_in_file("cpp-netlib/CMakeLists.txt", "include(GNUInstallDirs)", conan_magic_lines)

        conan_magic_lines = '''if (OPENSSL_FOUND)
message("**************************************************************")
    '''
        replace_in_file("cpp-netlib/CMakeLists.txt", "if (OPENSSL_FOUND)", conan_magic_lines)

        replace_in_file("cpp-netlib/CMakeLists.txt",
                        "file(RELATIVE_PATH REL_INCLUDE_DIR \"${INSTALL_CMAKE_DIR}\"",
                        "#file(RELATIVE_PATH REL_INCLUDE_DIR \"${INSTALL_CMAKE_DIR}\"")
        replace_in_file("cpp-netlib/CMakeLists.txt",
                        "    \"${CMAKE_INSTALL_FULL_INCLUDEDIR}\")",
                        "#    \"${CMAKE_INSTALL_FULL_INCLUDEDIR}\")")

        cmake = CMake(self.settings)

        cmake_options = []
        for option_name in self.options.values.fields:
            activated = getattr(self.options, option_name)
            the_option = "%s=" % option_name.upper()
            if option_name == "shared":
               the_option = "CPP-NETLIB_BUILD_SHARED_LIBS=ON" if activated else "CPP-NETLIB_BUILD_SHARED_LIBS=OFF"
            elif option_name == "enable_https":
               the_option = "CPP-NETLIB_ENABLE_HTTPS=ON" if activated else "CPP-NETLIB_ENABLE_HTTPS=OFF"
            elif option_name == "enable_tests":
               the_option = "CPP-NETLIB_BUILD_TESTS=ON" if activated else "CPP-NETLIB_BUILD_TESTS=OFF"
            elif option_name == "enable_examples":
               the_option = "CPP-NETLIB_BUILD_EXAMPLES=ON" if activated else "CPP-NETLIB_BUILD_EXAMPLES=OFF"
            else:
               the_option += "ON" if activated else "OFF"
            cmake_options.append(the_option)

        cmake_cmd_options = " -D".join(cmake_options)

        cmake_conf_command = 'cmake %s/cpp-netlib %s -DCMAKE_INSTALL_PREFIX:PATH=install -D%s' % (self.conanfile_directory, cmake.command_line, cmake_cmd_options)
        self.output.warn(cmake_conf_command)
        self.run(cmake_conf_command)

        self.run("cmake --build . --target install %s" % cmake.build_config)

    def imports(self):
        self.copy("*.dll", dst="bin", src="bin")
        self.copy("*.dylib*", dst="bin", src="lib")

    def package(self):
        self.copy("*.hpp", dst="include", src="install/include")
        self.copy("*.ipp", dst="include", src="install/include")
        self.copy("*.hpp", dst="include", src="cpp-netlib/deps/asio/asio/include")
        self.copy("*.ipp", dst="include", src="cpp-netlib/deps/asio/asio/include")
        self.copy("*.dll", dst="bin", src="install/install/bin")
        self.copy("*.lib", dst="lib", src="install/install/lib")
        self.copy("*.a", dst="lib", src="install/install/lib")
        self.copy("*.so*", dst="lib", src="install/install/lib")
        self.copy("*.dylib", dst="lib", src="install/install/lib")
        self.copy("*.*", dst="lib/CMake", src="install/install/CMake")

    def package_info(self):
        self.cpp_info.libs = ["cppnetlib-uri", "cppnetlib-client-connections", "cppnetlib-server-parsers"]

        if self.settings.compiler == "gcc" or self.settings.compiler == "apple-clang":
            self.cpp_info.cppflags = ["-std=c++11"]
